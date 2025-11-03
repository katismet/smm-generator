from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from vk_api import VkApi, upload

from src.config import VK_API_KEY, VK_GROUP_ID


@dataclass
class PostResult:
    full_id: str
    post_id: str


class VKPublisher:
    """
    Публикация постов в VK через официальный API.
    Используем vk_api library для удобства работы с VK API.
    """

    def __init__(self, api_key: Optional[str] = None, group_id: Optional[int] = None):
        self.api_key = api_key or VK_API_KEY
        self.group_id = group_id or VK_GROUP_ID

        # Инициализация сессии VK API
        self.vk_session = VkApi(token=self.api_key)
        self.vk = self.vk_session.get_api()

    def upload_photo(self, image_path: Path | str) -> str:
        """
        Загрузка фото на сервер VK и получение photo_id.
        :param image_path: Путь к изображению.
        :return: photo_id в формате "group_id_photo_id"
        """
        # Получаем URL сервера для загрузки
        upload_url = self.vk.photos.getWallUploadServer(group_id=abs(self.group_id))["upload_url"]

        # Загружаем файл
        image_path = Path(image_path)
        with open(image_path, "rb") as f:
            files = {"photo": (image_path.name, f, "image/png")}
            upload_response = requests.post(upload_url, files=files)

        upload_data = upload_response.json()

        # Сохраняем фото в группе
        save_response = self.vk.photos.saveWallPhoto(
            group_id=abs(self.group_id),
            server=upload_data["server"],
            photo=upload_data["photo"],
            hash=upload_data["hash"],
        )

        photo_id = save_response[0]["id"]
        owner_id = save_response[0]["owner_id"]

        return f"{owner_id}_{photo_id}"

    def publish_post(
        self,
        text: str,
        image_path: Optional[Path | str] = None,
        *,
        from_group: bool = True,
    ) -> PostResult:
        """
        Публикация поста на стену группы.
        :param text: Текст поста.
        :param image_path: Путь к изображению (опционально).
        :param from_group: Публиковать от имени группы (True) или от себя (False).
        :return: PostResult с full_id поста.
        """
        # Отрицательный owner_id для группы
        owner_id = -abs(self.group_id)

        attachments = []
        # Загружаем фото, если есть
        if image_path:
            photo_id = self.upload_photo(image_path)
            attachments.append(f"photo{photo_id}")

        # Публикуем пост
        params = {
            "owner_id": owner_id,
            "message": text,
            "from_group": 1 if from_group else 0,
        }
        if attachments:
            params["attachments"] = attachments

        result = self.vk.wall.post(**params)

        post_id = str(result["post_id"])
        full_id = f"{owner_id}_{post_id}"

        return PostResult(full_id=full_id, post_id=post_id)

