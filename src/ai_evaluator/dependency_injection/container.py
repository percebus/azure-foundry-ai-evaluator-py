from logging import Logger

from azure.ai.evaluation import AzureOpenAIModelConfiguration, ContentSafetyEvaluator, GroundednessEvaluator, QAEvaluator, ViolenceEvaluator
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from azure.ai.evaluation._model_configurations import EvaluatorConfig
from azure.ai.projects import AIProjectClient
from azure.core.credentials import AccessToken, TokenCredential
from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv
from lagom import Container
from lagom.interfaces import ReadableContainer

from ai_evaluator.config.logs import LoggingConfig
from ai_evaluator.config.os_environ.azure_openai import AzureOpenAISettings
from ai_evaluator.config.os_environ.settings import Settings

container = Container()


def create_settings(ctr: ReadableContainer) -> Settings:
    load_dotenv()  # FIXME? move to main.py?
    settings = Settings()  # pyright: ignore[reportCallIssue]

    # return Singleton(settings) # TODO
    return settings


def get_token(ctr: ReadableContainer) -> str:
    azure_openai_settings = ctr[AzureOpenAISettings]
    return azure_openai_settings.api_key if azure_openai_settings.api_key else ctr[AccessToken].token


container[Settings] = create_settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai

container[LoggingConfig] = LoggingConfig
container[Logger] = lambda c: c[LoggingConfig].logger

container[AzureCliCredential] = AzureCliCredential
container[DefaultAzureCredential] = DefaultAzureCredential

# Choose either / or
# container[TokenCredential] = lambda c: c[AzureCliCredential]
container[TokenCredential] = lambda c: c[DefaultAzureCredential]

container[AccessToken] = lambda c: c[TokenCredential].get_token("https://cognitiveservices.azure.com/.default")

container[AIProjectClient] = lambda c: AIProjectClient(
    endpoint=c[Settings].azure_ai_project_endpoint,
    credential=container[TokenCredential],  # pyright: ignore[reportArgumentType]
)

# fmt: off
container[AzureOpenAIModelConfiguration] = lambda c: AzureOpenAIModelConfiguration(
    azure_endpoint=c[AzureOpenAISettings].base_url,
    azure_deployment=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version,
    api_key=get_token(c),
    # api_key=c[AzureOpenAISettings].api_key,
)
# fmt: on


# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#composite-evaluators
# NOTE: Includes
# - CoherenceEvaluator
# - FluencyEvaluator
# - F1ScoreEvaluator
# - GroundednessEvaluator
# - RelevanceEvaluator
# - SimilarityEvaluator
container[QAEvaluator] = lambda c: QAEvaluator(model_config=c[AzureOpenAIModelConfiguration])
container[GroundednessEvaluator] = lambda c: GroundednessEvaluator(model_config=c[AzureOpenAIModelConfiguration])

# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#composite-evaluators
# NOTE: Includes
# - HateUnfairnessEvaluator
# - SelfHarmEvaluator
# - SexualEvaluator
# - ViolenceEvaluator
container[ContentSafetyEvaluator] = lambda c: ContentSafetyEvaluator(
    credential=c[DefaultAzureCredential],
    azure_ai_project=c[Settings].azure_ai_project_endpoint,
)

container[ViolenceEvaluator] = lambda c: ViolenceEvaluator(
    credential=c[DefaultAzureCredential],
    azure_ai_project=c[Settings].azure_ai_project_endpoint,
)

# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#evaluator-parameter-format
container[dict[str, EvaluatorBase[str | float]]] = lambda c: {
    "qa": c[QAEvaluator],
    "content_safety": c[ContentSafetyEvaluator],
}

container[dict[str, EvaluatorConfig]] = (
    lambda c: {
        # i.e.
        # "groundedness": {  # EvaluatorConfig(  # TODO TypedDict
        #     "query": "${data.query}",
        #     "context": "${data.context}",
        #     "response": "${data.response}",
        # }
    }
)
