from logging import Logger

from hamcrest import assert_that, instance_of, is_, not_none

from ai_evaluator.config.logs import LoggingConfig


def test__logging_config__is_instance_of__LoggingConfig(logging_config: LoggingConfig):
    assert_that(logging_config, is_(not_none()))
    assert_that(logging_config, is_(instance_of(LoggingConfig)))


def test__logger__is_instance_of__Logger(logging_config: LoggingConfig):
    """This test demonstrates that config/logging.conf gets loaded.
    And then a new `logger` instance is created."""

    logger: Logger = logging_config.logger
    assert_that(logger, is_(not_none()))
    assert_that(logger, is_(instance_of(Logger)))
