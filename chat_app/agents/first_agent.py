from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent, RunContext
from typing import Optional
import logfire


logfire.configure()

model = OllamaModel(
    'qwen2.5:3b',
    provider=OllamaProvider(
        base_url='http://localhost:11434/v1',
    ),
)

first_agent = Agent(
    model,
    system_prompt=(
        "You are a ChatBot asistant for users. "
        "Your task will be generating Users, Posts, Todos, and Comments and provide a comprehansive summaries based only on tool results"
        
        "SEARCH GUIDELINES:\n"
        "1. When searching, use only Users names, Posts, Todos, and Comments. "
        
        "RULES:\n"
        "1. Always use the 'search_records' first to find live data.\n"
        "2. If 'search_records' finds nothing, use 'search_knowledge_base'.\n"
        "3. If BOTH tools return no results, state clearly: 'No records found matching your query.'\n"
        "4. NEVER invent Users names, Posts, Todos, and Comments.\n"
        "5. Clearly distinguish between 'Live Records' (from search_records) and 'Historical Archives' (from search_knowledge_base).\n"
        "6. NEVER type JSON. NEVER explain your process. Just provide the final summary."
    )
)

@first_agent.tool
async def search_records(
    ctx: RunContext[None],
    query: str = "",
    time_preset: Optional[str] = None,
    status: Optional[str] = None
)->str:
    
    data = await search_records(
        query=query,
        limit=10,
        time_preset=time_preset,
        status=status
    )
    
    if "error" in data:
        return data["error"]
    
    results = data.get("results", {})
    
    