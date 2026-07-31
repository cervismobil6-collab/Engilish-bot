"""
OpenAI integration service
"""

import logging
from openai import AsyncOpenAI
from config import config
from ai.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


async def ask_ai_tutor(question: str, user_context: dict = None) -> str:
    """
    Ask AI tutor a question about English
    """
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
        
        response = await client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            max_tokens=config.OPENAI_MAX_TOKENS,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "❌ AI Ustoz vaqti-vaqti bilan bo'rin xizmat ko'rsatmoqda. Qayta urinib ko'ring."


async def check_grammar(text: str) -> dict:
    """
    Check grammar and provide corrections
    """
    prompt = f"""Ushbu Ingliz tilidagi gapni tekshiring va xatolar bo'lsa ularni to'g'ri qiling:

"{text}"

Javob quyidagi formatda bo'lsin:
✅ To'g'ri/❌ Xato
Xatolar: (agar bo'lsa)
To'g'ri versiya: (agar xato bo'lsa)
Tushuntirish: (xatoning sababini tushuntirish)
    """
    
    response = await ask_ai_tutor(prompt)
    return {"result": response}
