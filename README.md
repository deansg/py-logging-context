# py-logging-context
A Python util for automatically adding extra log fields to logs.

Example usage:
```python
from py-logging-context import LoggingContext

logger = get_logger()

with LoggingContext(request_id="some-id", user_name="John Doe"):
    logger.info("Hello world!")  # log record will include `request_id` and `user_name` fields
```

This library is implemented using Python's [Context Variables](https://docs.python.org/3/library/contextvars.html), and 
therefore works both in multithreaded settings and with `asyncio`. Therefore, it is superior to solutions based on
thread-local data, which will not work with async functions well.
