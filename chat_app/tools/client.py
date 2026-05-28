import httpx, asyncio, json
from typing import Any, List, Dict
from dotenv import load_dotenv
import logfire
import os

load_dotenv()
logfire.configure()

JSONPLACEHOLDER_URL = os.getenv("JSONPLACEHOLDER_URL", "https://jsonplaceholder.typicode.com")

#searches records using dynamic query parameters
async def search_user_records(**query_params:Any) -> List[Dict[str,Any]]:
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
            
            users = response.json()
            logfire.info(f"Retrieved {len(users)} user(s) matching criteria: {query_params}")
            
            return users
        
        
        except httpx.HTTPStatusError as exc:
            logfire.erro(f"HTTP {exc.response.status_code} error requesting {exc.request.url}")
            raise
            
        except httpx.RequestError as exc:
            logfire.error(f"Network error occurred requesting {exc.request.url}")
            raise
        
if __name__ == "__main__":
    users = asyncio.run(search_user_records(username="Bret"))
    if users:
        bret_data = users[0]
        
        print(json.dumps(bret_data, indent=4))
    print(f"Found user: {users[0].get('name') if users else 'None'}")