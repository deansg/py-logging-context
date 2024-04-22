import logging
import unittest

from py_logging_context import LoggingContextInjectingFilter, LoggingContext


class TestLoggingContext(unittest.TestCase):
    # noinspection PyUnresolvedReferences
    def test_sanity(self):
        logger = logging.getLogger()
        logger.addFilter(LoggingContextInjectingFilter())

        with LoggingContext(test_field_1="val1", test_field_2="val2"):
            with self.assertLogs(logger) as cm:
                logger.info("hello world")

                records = cm.records
                self.assertEqual(1, len(records))
                record = records[0]
                self.assertEqual(record.test_field_1, "val1")
                self.assertEqual(record.test_field_2, "val2")
                self.assertEqual("hello world", record.msg)


if __name__ == '__main__':
    unittest.main()
