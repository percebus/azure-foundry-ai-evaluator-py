from collections.abc import Generator
from logging import Logger
from unittest.mock import MagicMock

import pytest
from azure.ai.evaluation import AzureOpenAIModelConfiguration, ContentSafetyEvaluator, QAEvaluator
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from azure.ai.evaluation._model_configurations import EvaluatorConfig
from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import DefaultAzureCredential
from hamcrest import assert_that, has_length, instance_of, is_
from lagom import Container

from ai_evaluator.config.os_environ.settings import Settings
from ai_evaluator.dependency_injection.container import container


@pytest.fixture()
def patched_container(
    settings: Settings,
    token_credential: TokenCredential,
    access_token: AccessToken,
) -> Generator[Container]:
    # Before each test
    # SRC: https://lagom-di.readthedocs.io/en/latest/testing_with_lagom/
    test_container = container.clone()
    test_container[Settings] = settings  # .env.test
    test_container[TokenCredential] = token_credential  # MagicMock
    test_container[AccessToken] = access_token  # MagicMock

    # During each test
    yield test_container

    # After each test
    test_container = None


def test__contains_instance_of__Settings(patched_container: Container) -> None:
    settings = patched_container[Settings]
    assert_that(settings, is_(instance_of(Settings)))


def test__contains_instance_of__Logger(patched_container: Container) -> None:
    logger = patched_container[Logger]
    assert_that(logger, is_(instance_of(Logger)))


def test__contains_instance_of__TokenCredential(patched_container: Container) -> None:
    credential = patched_container[TokenCredential]
    assert_that(credential, is_(instance_of(TokenCredential)))


def test__contains_instance_of__DefaultAzureCredential(patched_container: Container) -> None:
    credential = patched_container[DefaultAzureCredential]
    assert_that(credential, is_(instance_of(DefaultAzureCredential)))
    assert_that(credential, is_(instance_of(TokenCredential)))


def test__contains_instance_of__AccessToken(patched_container: Container) -> None:
    access_token = patched_container[AccessToken]
    assert_that(access_token, is_(instance_of(AccessToken)))
    assert_that(access_token, is_(instance_of(MagicMock)))


def test__contains_instance_of__AzureOpenAIModelConfiguration(patched_container: Container) -> None:
    azure_openai_model_configuration = patched_container[AzureOpenAIModelConfiguration]
    assert_that(azure_openai_model_configuration, is_(instance_of(dict)))  # TypedDict


def test__contains_instance_of__QAEvaluator(patched_container: Container) -> None:
    qa_evaluator = patched_container[QAEvaluator]
    assert_that(qa_evaluator, is_(instance_of(QAEvaluator)))


def test__contains_instance_of__ContentSafetyEvaluator(patched_container: Container) -> None:
    content_safety_evaluator = patched_container[ContentSafetyEvaluator]
    assert_that(content_safety_evaluator, is_(instance_of(ContentSafetyEvaluator)))


def test__contains_instance_of__dict_str_EvaluatorBase(patched_container: Container) -> None:
    evaluators = patched_container[dict[str, EvaluatorBase[str | float]]]
    assert_that(evaluators, is_(instance_of(dict)))
    assert_that(evaluators, has_length(2))

    assert_that(evaluators["qa"], is_(instance_of(QAEvaluator)))
    assert_that(evaluators["content_safety"], is_(instance_of(ContentSafetyEvaluator)))

    # FIXME different instances
    # fmt: off
    # assert_that(evaluators, has_entries({
    #     "qa": qa_evaluator,
    #     "content_safety": content_safety_evaluator}))
    # fmt: on


def test__contains_instance_of__dict_str_EvaluatorConfig(patched_container: Container) -> None:
    evaluators = patched_container[dict[str, EvaluatorConfig]]
    assert_that(evaluators, is_(instance_of(dict)))
