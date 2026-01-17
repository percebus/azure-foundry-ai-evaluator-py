from typing import Generator
from unittest.mock import MagicMock

import pytest
from azure.core.credentials import TokenCredential
from azure.ai.projects import AIProjectClient

from ai_evaluator.config.logs import LoggingConfig
from ai_evaluator.config.os_environ.settings import Settings


@pytest.fixture()
def settings() -> Generator[Settings, None, None]:
    # Before each test
    settings = Settings()  # pyright: ignore[reportCallIssue]

    # During each test
    yield settings

    # After each test
    settings = None


@pytest.fixture()
def logging_config() -> Generator[LoggingConfig, None, None]:
    # Before each test
    logging_config = LoggingConfig()

    # During each test
    yield logging_config

    # After each test
    logging_config = None


@pytest.fixture()
def token_credential() -> Generator[TokenCredential, None, None]:
    # Before each test
    credential = MagicMock(spec=TokenCredential)

    # During each test
    yield credential

    # After each test
    credential = None


@pytest.fixture()
def ai_project_client() -> Generator[AIProjectClient, None, None]:
    # Before each test
    ai_project_client = MagicMock(spec=AIProjectClient)

    # During each test
    yield ai_project_client

    # After each test
    ai_project_client = None
