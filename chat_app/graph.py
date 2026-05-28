from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from pydantic_ai.models.ollama import OllamaModel
from pydantic import BaseModel
from pydantic_ai.providers.ollama import OllamaProvider
from typing import Literal
from typing import(
    TypedDict, Annotated
)


memory = MemorySaver()

model = OllamaModel(
    'qwen2.5:3b',
    provider=OllamaProvider(
        base_url='http://localhost:11434/v1',
    ),
    
)

#makes a lists of messages and avoid duplicating messages
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class RouterSchema(BaseModel):
    destination: Literal["admin_agent", "supervisor"]
    
    

    
