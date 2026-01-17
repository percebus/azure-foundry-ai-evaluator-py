from collections.abc import Generator

import pytest
from hamcrest import assert_that, equal_to, instance_of, is_, is_not, none, not_, not_none

from ai_evaluator.config.os_environ.azure_openai import AzureOpenAISettings
from ai_evaluator.config.os_environ.settings import Settings


@pytest.fixture()
def azure_openai_settings(settings: Settings) -> Generator[AzureOpenAISettings]:
    yield settings.azure_openai


def test__azure_openai__is_instance_of__AzureOpenAISettings(azure_openai_settings: AzureOpenAISettings):
    assert_that(azure_openai_settings, is_(not_none()))
    assert_that(azure_openai_settings, is_(instance_of(AzureOpenAISettings)))


def test__base_url__equals__env_test(azure_openai_settings: AzureOpenAISettings):
    # AZURE_OPENAI__BASE_URL
    base_url = str(azure_openai_settings.base_url)
    assert_that(base_url, not_(equal_to("")))
    assert_that(
        base_url, equal_to("https://some.services.ai.azure.com/openai/deployments/some-deployment/chat/completions?api-version=some-version")
    )  # .env.test


def test__deployment__equals__env_test(azure_openai_settings: AzureOpenAISettings):
    # AZURE_OPENAI__DEPLOYMENT
    deployment_name = str(azure_openai_settings.deployment_name)
    assert_that(deployment_name, not_(equal_to("")))
    assert_that(deployment_name, equal_to("some-deployment"))  # .env.test


def test__api_key__equals__env_test(azure_openai_settings: AzureOpenAISettings):
    # AZURE_OPENAI__API_KEY
    api_key = str(azure_openai_settings.api_key)
    assert_that(api_key, is_not(none()))  # .env
    assert_that(api_key, equal_to("shhh"))  # .env.test
