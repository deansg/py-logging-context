# py-logging-context

A Python util for automatically adding extra log fields to logs.

### Installation

This project is published to [PyPI](https://pypi.org/project/py-logging-context/0.1.0/) and can be installed using:

`pip install py-logging-context==0.1.1`

### Example Usage

```python
import logging
from py_logging_context import LoggingContext, LoggingContextInjectingFilter

logger = logging.getLogger()
logger.addFilter(LoggingContextInjectingFilter())

with LoggingContext(request_id="some-id", user_name="John Doe"):
    logger.info("Hello world!")  # log record will include `request_id` and `user_name` fields
```

This library is implemented using Python's [Context Variables](https://docs.python.org/3/library/contextvars.html), and
therefore works in multithreaded settings as well `asyncio`. This is in contrast to solutions based on
thread-local data, which will not work as intended async functions (such as
[log-with-context](https://github.com/neocrym/log-with-context/tree/main)).

This is a lightweight library and has no additional dependencies.
