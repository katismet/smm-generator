from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from openai import OpenAI
from src.config import OPENAI_API_KEY


DEFAULT_SIZE = "1024x1024"  # для dall-e-3: "1024x1024", "1792x1024", "1024x1792"


@dataclass
class ImageResult:
    path: Path
    size: str


class ImageGenerator:
    """
    Генерация изображения через OpenAI Images (gpt-image-1).
    Используем b64_json, чтобы не зависеть от временных URL.
    """

    def __init__(self, api_key: Optional[str] = None, *, model: str = "dall-e-3"):
        self.client = OpenAI(api_key=api_key or OPENAI_API_KEY)
        self.model = model

    def generate_image(
        self,
        prompt: str,
        *,
        size: str = DEFAULT_SIZE,
        out_dir: str | Path = "outputs/images",
        filename: Optional[str] = None,
    ) -> ImageResult:
        """
        :param prompt: Краткое предметное описание сцены (без стилей/камер/художников).
        :param size: Размер, например "1024x1024".
        :param out_dir: Папка, куда сохраняем PNG.
        :param filename: Необязательное имя файла (без пути).
        :return: ImageResult с путём к сохранённому PNG.
        """
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Генерация
        resp = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
        )

        url = resp.data[0].url
        if not url:
            raise RuntimeError("Empty image URL from OpenAI Images API")

        # Скачиваем изображение по URL
        image_bytes = requests.get(url).content

        # Имя файла
        if filename:
            name = filename if filename.lower().endswith(".png") else f"{filename}.png"
        else:
            # безопасное имя из первых слов промпта
            safe = "_".join(prompt.strip().lower().split()[:6])
            if not safe:
                safe = "image"
            name = f"{safe}.png"

        out_path = out_dir / name

        # Если файл уже есть — добавим суффикс
        i = 1
        while out_path.exists():
            stem = out_path.stem
            out_path = out_path.with_stem(f"{stem}_{i}")
            i += 1

        out_path.write_bytes(image_bytes)
        return ImageResult(path=out_path, size=size)

