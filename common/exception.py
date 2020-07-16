import functools

from sanic.handlers import ErrorHandler
from sanic.exceptions import ServerError


class CustomErrorHandler(ErrorHandler):

    def default(self, request, exception):
        ''' handles errors that have no error handlers assigned '''
        # You custom error handling logic...
        return super().default(request, exception)
