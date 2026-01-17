from hamcrest import assert_that, equal_to, instance_of, is_, is_not, not_, not_none

from ai_evaluator.config.os_environ.azure_openai import AzureOpenAISettings
from ai_evaluator.config.os_environ.settings import Settings


def test__settings__is_instance_of__Settings(settings: Settings):
    assert_that(settings, is_(not_none()))
    assert_that(settings, is_(instance_of(Settings)))


def test__environment__equals__test(settings: Settings):
    # ENVIRONMENT
    assert_that(settings.environment, not_(equal_to("")))  # Settings
    assert_that(settings.environment, equal_to("test"))  # .env.test


def test__dry_run__is__True(settings: Settings):
    # DRY_RUN
    assert_that(settings.dry_run, is_not(False))  # .env
    assert_that(settings.dry_run, is_(True))  # .env.test


def test__azure_ai_project_endpoint__equals__env_test(settings: Settings):
    # AZURE_AI_PROJECT_ENDPOINT
    azure_ai_project_endpoint = str(settings.azure_ai_project_endpoint)
    assert_that(azure_ai_project_endpoint, not_(equal_to("")))  # .env
    assert_that(azure_ai_project_endpoint, equal_to("https://some.services.ai.azure.com/api/projects/here"))  # .env.test


def test__azure_openai__is__instance_of_AzureOpenAISettings(settings: Settings):
    # AZURE_OPENAI_*
    azure_openai_settings = settings.azure_openai
    assert_that(azure_openai_settings, is_(not_none()))
    assert_that(azure_openai_settings, is_(instance_of(AzureOpenAISettings)))
