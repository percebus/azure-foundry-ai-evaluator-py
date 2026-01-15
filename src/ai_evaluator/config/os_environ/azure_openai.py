from pydantic import BaseModel, Field


class AzureOpenAISettings(BaseModel):
    base_url: str = Field()

    deployment_name: str = Field()

    api_version: str = Field()

    api_key: str | None = Field(default=None)
