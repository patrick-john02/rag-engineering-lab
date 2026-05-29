import httpx, asyncio, json
from typing import Any, List, Dict
from dotenv import load_dotenv
from pydantic import BaseModel, TypeAdapter
from chat_app.schemas.typicode_schema import(
    User, Todos, Post
)
import logfire
import os

load_dotenv()
logfire.configure()

JSONPLACEHOLDER_URL = os.getenv("JSONPLACEHOLDER_URL", "https://jsonplaceholder.typicode.com")


UserListAdapter = TypeAdapter(List[User])
TodoListAdapter = TypeAdapter(List[Todos])
PostListAdapter = TypeAdapter(List[Post])


#searches and validate records using dynamic query parameters
async def search_user_records(**query_params:Any) -> List[User]:
    
    if not query_params:
        logfire.warn("No search parameters provided.")
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JSONPLACEHOLDER_URL}/users",
                params=query_params,
                timeout=5.0
            )
            response.raise_for_status()
            
            raw_users = response.json()
            validate_user = UserListAdapter.validate_python(raw_users)
            
            
            logfire.info(f"Retrieved {len(validate_user)}")
            

            return validate_user
        
        
        except httpx.HTTPStatusError as exc:
            logfire.error(f"HTTP {exc.response.status_code} error requesting {exc.request.url}")
            raise
            
        except httpx.RequestError as exc:
            logfire.error(f"Network error occurred requesting {exc.request.url}")
            raise
        
        except Exception as e:
            logfire.error(f"Unexpected error in search_user_records:{str(e)}")

async def search_todo_records(**query_params:Any) -> List[Todos]:
    
    if not query_params:
        logfire.warn("No search parameters provided")
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JSONPLACEHOLDER_URL}/todos",
                params=query_params,
                timeout=5.0
            )
            
            response.raise_for_status()
            raw_todos = response.json()
            validate_todos = TodoListAdapter.validate_python(raw_todos)
            
            logfire.info(f"Retrieved {len(validate_todos)}")
        
            return validate_todos
        
        except httpx.HTTPStatusError as exc:
            logfire.error(f"HTTP {exc.response.status_code} error requesting {exc.request.url}")
            raise
        
        except httpx.RequestError as exc:
            logfire.error(f"Network error occurred requesting {exc.request.url}")
            raise
        
        except Exception as e:
            logfire.error(f"Unexpected error in search_todo_records: {str(e)}")
            
async def search_post_records(**query_params:Any) -> List[Post]:
    
    if not query_params:
        logfire.warn("No search parameters provided")
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JSONPLACEHOLDER_URL}/posts",
                params=query_params,
                timeout=5.0
            )
            
            response.raise_for_status()
            raw_posts = response.json()
            validate_posts = PostListAdapter.validate_python(raw_posts)
            
            logfire.info(f"Retrieved{len(validate_posts)}")
            
            return validate_posts
        
        except httpx.HTTPStatusError as exc:
            logfire.error(f"HTTP {exc.response.status_code} error requesting {exc.request.url}")
            
            
        except httpx.RequestError as exc:
            logfire.error(f"Netowkr error occurred requesting {exc.request.url}")
            raise
        
        except Exception as e:
            logfire.error(f"Unexpected error in search_post_records:{str(e)}")
            

        
        



#testing
# if __name__ == "__main__":
#     users = asyncio.run(search_user_records(username="Bret"))
#     if users:
#         target_user = users[0]
        
#         print(f"Name: {target_user.name}")
#         print(f"Company Name: {target_user.company.name}")
        
#         print(f"Latitude (as Float): {target_user.address.geo.lat}")
#         print(f"Latitude Type: {type(target_user.address.geo.lat)}")
#     else:
#         print("User not found.") 