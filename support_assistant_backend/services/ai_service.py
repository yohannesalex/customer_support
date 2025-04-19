import aiohttp
from support_assistant_backend.core.config import settings

class AIService:
    # ← Updated to the OpenAI‐compatible chat completions endpoint
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"  # :contentReference[oaicite:0]{index=0}

    async def stream_response(self, prompt: str):
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        # Build an OpenAI‐style chat payload with streaming enabled
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a helpful support assistant."},
                {"role": "user",   "content": prompt}
            ],
            "stream": True  # ← tell the API to stream results :contentReference[oaicite:1]{index=1}
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(self.BASE_URL, json=payload) as resp:
                # resp.content yields raw byte chunks as soon as they arrive
                async for chunk in resp.content:
                    yield chunk.decode("utf-8")
