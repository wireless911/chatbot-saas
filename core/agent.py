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
    pass


