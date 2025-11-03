from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from src.config import OPENAI_API_KEY


# ---- Pydantic-схема результата ----
class PostPayload(BaseModel):
    title: str = Field(..., description="Короткий заголовок поста, до 60 символов, без эмодзи.")
    post_text: str = Field(
        ...,
        description="Основной текст поста 500–900 символов, без воды, с конкретикой, без эмодзи.",
    )
    image_prompt: str = Field(
        ...,
        description="Краткое (1–2 предложения) описательное ТЗ для изображения, без стиля, без камеры.",
    )
    hashtags: List[str] = Field(
        default_factory=list,
        description="До 5 хэштегов в нижнем регистре без пробелов (#word).",
        max_items=5,
    )


# ---- Обёртка результата для удобства ----
@dataclass
class PostResult:
    title: str
    text: str
    image_prompt: str
    hashtags: List[str]

    @property
    def pretty(self) -> str:
        tags = " ".join(self.hashtags) if self.hashtags else ""
        return f"{self.title}\n\n{self.text}\n\n{tags}".strip()


class PostGenerator:
    """
    Генератор постов (OpenAI Responses API).
    Современно на 27.10.2025: используем responses.create + json_schema.
    """

    def __init__(self, api_key: Optional[str] = None, *, model: str = "gpt-4.1-mini"):
        self.client = OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.model = model

    def generate_post(
        self,
        topic: str,
        *,
        tone: str = "деловой и дружелюбный",
        audience: str = "подписчики в VK",
        brand: Optional[str] = None,
        locale: str = "ru",
    ) -> PostResult:
        """
        :param topic: Тематика/повод поста (наша своя тема по условию ДЗ).
        :param tone: Тональность.
        :param audience: Целевая аудитория.
        :param brand: Необязательное имя бренда.
        :param locale: Язык.
        """

        sys = (
            "Ты профессиональный SMM-копирайтер. Пиши на русском. "
            "Строго без эмодзи, без markdown-оформления, без буллетов. "
            "Короткие абзацы по 2–4 предложения. Без воды и общих фраз. "
            "Дай конкретику, выгоды, детали. Хэштеги в нижнем регистре, максимум 5. "
            "Верни результат в формате JSON с полями: title, post_text, image_prompt, hashtags (массив до 5 строк)."
        )

        user = (
            f"Тема поста: {topic}\n"
            f"Тональность: {tone}\n"
            f"Аудитория: {audience}\n"
            f"Бренд: {brand or 'без упоминаний бренда'}\n"
            f"Требование к картинке: опиши предметно содержимое сцены для генерации изображения "
            f"(1–2 предложения), без стиля и без упоминания художников/камеры."
        )

        # JSON-схема для строгой структурной выдачи
        schema = {
            "name": "PostPayload",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "post_text": {"type": "string"},
                    "image_prompt": {"type": "string"},
                    "hashtags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "maxItems": 5,
                    },
                },
                "required": ["title", "post_text", "image_prompt"],
                "additionalProperties": False,
            },
            "strict": True,
        }

        # Используем Chat Completions API с structured outputs
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": sys},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )

        raw = resp.choices[0].message.content
        try:
            data = json.loads(raw)
            payload = PostPayload.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            raise RuntimeError(f"Invalid model output: {e}\nRaw: {raw}") from e

        # Нормализация хэштегов
        tags: List[str] = []
        for t in payload.hashtags or []:
            t = t.strip()
            if not t:
                continue
            if not t.startswith("#"):
                t = f"#{t}"
            tags.append(t.lower())

        return PostResult(
            title=payload.title.strip(),
            text=payload.post_text.strip(),
            image_prompt=payload.image_prompt.strip(),
            hashtags=tags[:5],
        )

