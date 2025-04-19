import aiohttp
from support_assistant_backend.core.config import settings

class AIService:
    BASE_URL = "https://api.groq.com/v1/stream"

    async def stream_response(self, prompt: str):
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.BASE_URL, json={"prompt": prompt}, headers=headers) as resp:
                async for chunk in resp.content:
                    yield chunk.decode()