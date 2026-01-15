from typing import Protocol

from ai_evaluator.models.conversation.message_protocol import MessageProtocol


class ConversationProtocol(Protocol):
    messages: list[MessageProtocol]
