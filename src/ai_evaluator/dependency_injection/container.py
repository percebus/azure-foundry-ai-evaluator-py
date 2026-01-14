from logging import Logger

from azure.ai.evaluation import AzureOpenAIModelConfiguration, ContentSafetyEvaluator, QAEvaluator
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from azure.ai.evaluation._model_configurations import EvaluatorConfig
from azure.ai.projects import AIProjectClient
from azure.core.credentials import TokenCredential
from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv
from lagom import Container, Singleton
from lagom.interfaces import ReadableContainer

from ai_evaluator.config.logs import LoggingConfig
from ai_evaluator.config.os_environ.azure_openai import AzureOpenAISettings
from ai_evaluator.config.os_environ.settings import Settings

container = Container()


def create_settings(ctr: ReadableContainer) -> Singleton[Settings]:
    load_dotenv()  # FIXME? move to main.py?
    return Singleton(Settings())  # pyright: ignore[reportCallIssue]


container[Settings] = create_settings
container[AzureOpenAISettings] = lambda c: c[Settings].azure_openai

container[LoggingConfig] = LoggingConfig
container[Logger] = lambda c: c[LoggingConfig].logger

container[AzureCliCredential] = AzureCliCredential
container[DefaultAzureCredential] = DefaultAzureCredential

# Choose either / or
# container[TokenCredential] = lambda c: c[AzureCl``iCredential]
container[TokenCredential] = lambda c: c[DefaultAzureCredential]

container[AIProjectClient] = lambda c: AIProjectClient(
    endpoint=c[Settings].azure_ai_project_endpoint,
    credential=container[TokenCredential],  # pyright: ignore[reportArgumentType]
)

# fmt: off
container[AzureOpenAIModelConfiguration] = lambda c: AzureOpenAIModelConfiguration(
    azure_endpoint=c[AzureOpenAISettings].base_url,
    azure_deployment=c[AzureOpenAISettings].deployment_name,
    api_version=c[AzureOpenAISettings].api_version,
    api_key=c[AzureOpenAISettings].api_key,
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

# SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk#evaluator-parameter-format
container[dict[str, EvaluatorBase[str | float]]] = lambda c: {
    "qa": c[QAEvaluator],
    "content_safety": c[ContentSafetyEvaluator],
}

container[dict[str, EvaluatorConfig]] = lambda c: {
    "groundedness": {  # EvaluatorConfig(  # TODO TypedDict
        "query": "${data.queries}",
        "context": "${data.context}",
        "response": "${data.response}",
    }
}
