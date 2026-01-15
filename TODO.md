# ai-evaluator

## TODOs

### New `azure.ai.evaluator` interface

```python
SRC: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk?view=foundry&preserve-view=true
TODO Use new APIs

testing_criteria = [
    {"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence"},
    {"type": "azure_ai_evaluator", "name": "groundedness", "evaluator_name": "builtin.groundedness"},
]

openai_client = project_client.get_openai_client()
eval_object = openai_client.evals.create(
    name="Agent Response Evaluation",
    data_source_config=data_source_config,
    testing_criteria=testing_criteria,
)

openai_client.evals.runs.create(
    eval_id=eval_object.id,
    name=f"Evaluation Run for Agent {agent.name}",
    data_source=data_source
)
```
