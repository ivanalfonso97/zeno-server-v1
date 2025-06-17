from typing import List, Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal['user', 'assistant'] = Field(..., description="The role of the message sender.")
    content: str = Field(..., description="The content of the message.")

class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="A list of chat messages in the conversation history.")