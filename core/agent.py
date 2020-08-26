#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：chatbot-management_v2 -> agent
@IDE    ：PyCharm
@Author ：Mr. Wireless
@Date   ：2020/7/9 17:59
@Desc   ：
==================================================
"""

import logging
import os
import shutil
import tempfile
import uuid
from asyncio import CancelledError
from typing import Any, Callable, Dict, List, Optional, Text, Tuple, Union

import aiohttp
from rasa.core.brokers.file import FileEventBroker
from sanic import Sanic

import rasa
import rasa.utils.io
import rasa.core.utils
from rasa.constants import (
    DEFAULT_DOMAIN_PATH,
    LEGACY_DOCS_BASE_URL,
    ENV_SANIC_BACKLOG,
    DEFAULT_CORE_SUBDIRECTORY_NAME,
)
from rasa.core import constants, jobs, training
from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from rasa.core.constants import DEFAULT_REQUEST_TIMEOUT
from rasa.core.domain import Domain
from rasa.core.exceptions import AgentNotReady
from rasa.core.interpreter import NaturalLanguageInterpreter, RegexInterpreter
from rasa.core.lock_store import LockStore, InMemoryLockStore
from rasa.core.nlg import NaturalLanguageGenerator
from rasa.core.policies.ensemble import PolicyEnsemble, SimplePolicyEnsemble
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.core.policies.policy import Policy
from rasa.core.processor import MessageProcessor
from rasa.core.tracker_store import (
    InMemoryTrackerStore,
    TrackerStore,
    FailSafeTrackerStore,
)
from rasa.core.trackers import DialogueStateTracker
from rasa.exceptions import ModelNotFound
from rasa.importers.importer import TrainingDataImporter
from rasa.model import (
    get_model_subdirectories,
    get_latest_model,
    unpack_model,
    get_model,
)
from rasa.nlu.utils import is_url
from rasa.utils.common import raise_warning, update_sanic_log_level
from rasa.utils.endpoints import EndpointConfig
from rasa.core.agent import Agent


class LSTMAgent(Agent):

    def __init__(self, *args, **kwargs):
        super(LSTMAgent, self).__init__(*args, **kwargs)

    @classmethod
    def load(
            cls,
            model_path: Text,
            interpreter: Optional[NaturalLanguageInterpreter] = None,
            generator: Union[EndpointConfig, NaturalLanguageGenerator] = None,
            tracker_store: Optional[TrackerStore] = None,
            lock_store: Optional[LockStore] = None,
            action_endpoint: Optional[EndpointConfig] = None,
            model_server: Optional[EndpointConfig] = None,
            remote_storage: Optional[Text] = None,
            path_to_model_archive: Optional[Text] = None,
    ) -> "Agent":
        """Load a persisted model from the passed path."""
        try:
            if not model_path:
                raise ModelNotFound("No path specified.")
            elif not os.path.exists(model_path):
                raise ModelNotFound(f"No file or directory at '{model_path}'.")
            elif os.path.isfile(model_path):
                model_path = get_model(model_path)
        except ModelNotFound:
            raise ValueError(
                "You are trying to load a MODEL from '{}', which is not possible. \n"
                "The model path should be a 'tar.gz' file or a directory "
                "containing the various model files in the sub-directories 'core' "
                "and 'nlu'. \n\nIf you want to load training data instead of "
                "a model, use `agent.load_data(...)` instead.".format(model_path)
            )

        core_model, nlu_model = get_model_subdirectories(model_path)

        if not interpreter and nlu_model:
            interpreter = NaturalLanguageInterpreter.create(nlu_model)

        domain = None
        ensemble = None

        if core_model:
            domain = Domain.load(os.path.join(core_model, DEFAULT_DOMAIN_PATH))
            ensemble = PolicyEnsemble.load(core_model) if core_model else None

            # ensures the domain hasn't changed between test and train
            domain.compare_with_specification(core_model)



        return cls(
            domain=domain,
            policies=ensemble,
            interpreter=interpreter,
            generator=generator,
            tracker_store=_tracker_store,
            lock_store=lock_store,
            action_endpoint=action_endpoint,
            model_directory=model_path,
            model_server=model_server,
            remote_storage=remote_storage,
            path_to_model_archive=path_to_model_archive,
        )
