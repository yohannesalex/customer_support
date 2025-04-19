import aiohttp
from support_assistant_backend.core.config import settings

class AIService:
    BASE_URL = "https://api.groq.com/v1/stream"

    async def stream_response(self, prompt: str):
        # Prepare headers with the Groq API key.
        headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
        # Create an aiohttp client session.
        async with aiohttp.ClientSession() as session:
            # Post the prompt to the Groq API for a streaming response.
            async with session.post(self.BASE_URL, json={"prompt": prompt}, headers=headers) as resp:
                # Asynchronously iterate through the response chunks.
                async for chunk in resp.content:
                    # Decode each chunk and yield it.
                    yield chunk.decode()