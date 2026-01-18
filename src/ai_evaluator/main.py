from typing import TYPE_CHECKING

from azure.ai.evaluation import evaluate  # pyright: ignore[reportUnknownVariableType]
from azure.ai.evaluation._evaluators._common._base_eval import EvaluatorBase
from azure.ai.evaluation._model_configurations import EvaluatorConfig
from lagom import Container

from ai_evaluator.config.os_environ.settings import Settings

if TYPE_CHECKING:
    from azure.ai.evaluation._evaluate._evaluate import EvaluationResult  # pyright: ignore[reportPrivateImportUsage]


def run(container: Container) -> None:
    dataset_path: str = "./data/input/conversation.jsonl"

    evaluators = container[dict[str, EvaluatorBase[str | float]]]
    evaluator_configurations = container[dict[str, EvaluatorConfig]]
    settings = container[Settings]

    evaluation_result: EvaluationResult = evaluate(
        data=dataset_path,
        evaluators=evaluators,  # pyright: ignore[reportArgumentType]
        evaluator_config=evaluator_configurations,  # pyright: ignore[reportUnknownArgumentType]
        output_path="data/output/evaluation_results.jsonl",
        azure_ai_project=settings.azure_ai_project_endpoint,  # FIXME
    )

    print(evaluation_result)


def main() -> None:
    from ai_evaluator.dependency_injection.container import container  # noqa: PLC0415

    run(container)


if __name__ == "__main__":
    main()
