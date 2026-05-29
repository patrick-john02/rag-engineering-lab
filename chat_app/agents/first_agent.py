from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai import Agent, RunContext
from typing import Optional, List
import logfire

from chat_app.schemas.typicode_schema import (
    User, Todos, Post
)
from chat_app.tools.client import (
    search_user_records,
    search_todo_records,
    search_post_records,
)

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
        "7. Do not explain the inner workings or tool names to the end user."
    )
)

@first_agent.tool
async def search_records(
    ctx: RunContext[None],
    username: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
    
    city: Optional[str] = None,
    suite: Optional[str] = None, 
    street: Optional[str] = None, 
    website: Optional[str] = None,
    company_name: Optional[str] = None,
)->str:
    try:
        query_params = {}
        if username: query_params["username"] = username
        if name: query_params["name"] = name
        if email: query_params["email"] = email
        if website: query_params["email"] = website
        
        if city:
            query_params["adress.city"] = city
            
        if suite:
            query_params["address.suite"] = suite
        
        if street:
            query_params["address.street"] = street
        
        if company_name:
            query_params["company.name"] = company_name
            
        
        if not query_params:
            return f"No user found matching those criteria"
        
        
        
        summary = "\n".join([
            f"ID: {u.id} | Name: {u.name} | Email: {u.email} | Address: {u.address.city} {u.address.street} {u.address.suite}"
            f"| Phone: {u.phone} | Website: {u.website} | Company : {u.company.name} "
            for u in query_params
        ])
        
        
        return f"Found {len(query_params)} user(s):\n{summary}"
        
    
    except Exception as e:
        logfire.error(f"Tool 'search_records' failed: {str(e)}")
        return f"Error: while searching records"
    
    
        
        
        