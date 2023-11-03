import contextvars
import logging
from typing import Dict, Iterable, List

_context_variables: Dict[str, contextvars.ContextVar] = {}
_CONTEXT_VARIABLE_NAME_PREFIX = "logging_context|"


class LoggingContextInjectingFilter(logging.Filter):
    """
    A filter which injects log fields that are added using LoggingContext instances into the log records
    """

    def filter(self, record: logging.LogRecord):
        extra_log_fields: Dict[str, any] = get_current_log_fields()
        for k, v in extra_log_fields.items():
            if v is not None:
                record.__dict__[k] = v
        return True


class LoggingContext:
    def __init__(self, **log_fields):
        self._tokens: List[contextvars.Token] = _add_log_fields(**log_fields)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _reset_log_fields(self._tokens)


def get_current_log_fields() -> Dict[str, any]:
    """
    Returned all log fields configured in the current context using LoggingContexts
    """
    return {k: v.get(None) for k, v in _context_variables.items()}


def remove_unused_context_vars(keys: List[str]):
    """
    Removes context variables representing log fields with the given keys (names). This is only necessary if the
    application using LoggingContexts has a very large/constantly increasing list of log fields used (only the number
    of field names is important, not values, and so this is probably a somewhat uncommon case).
    """
    return list(filter(None, (_context_variables.pop(key, None) for key in keys)))


def _add_log_fields(**log_fields) -> List[contextvars.Token]:
    tokens = []
    for k, v in log_fields.items():
        cur_variable = _context_variables.get(k)
        if cur_variable is None:
            cur_variable = _context_variables[k] = contextvars.ContextVar(
                f"{_CONTEXT_VARIABLE_NAME_PREFIX}{k}")
        tokens.append(cur_variable.set(v))
    return tokens


def _reset_log_fields(tokens: Iterable[contextvars.Token]):
    for token in tokens:
        token.var.reset(token)
