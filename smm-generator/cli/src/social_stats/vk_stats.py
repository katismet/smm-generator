from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from src.config import VK_API_KEY, VK_GROUP_ID

VK_API_URL = "https://api.vk.com/method"
VK_API_VERSION = "5.199"


@dataclass
class PostStat:
    post_id: int
    date: int  # unix
    text_preview: str
    likes: int
    comments: int
    reposts: int
    views: int


@dataclass
class StatsSummary:
    posts_count: int
    likes_total: int
    comments_total: int
    reposts_total: int
    views_total: int
    followers: Optional[int]
    posts: List[PostStat]


def _vk_call(method: str, **params) -> Dict[str, Any]:
    params.update({"access_token": VK_API_KEY, "v": VK_API_VERSION})
    r = requests.post(f"{VK_API_URL}/{method}", data=params, timeout=30)
    j = r.json()
    if "error" in j:
        raise RuntimeError(f"VK API error in {method}: {j['error']}")
    return j["response"]


def get_group_followers_count(group_id: int) -> Optional[int]:
    # fields=members_count вернет текущее число подписчиков
    try:
        resp = _vk_call(
            "groups.getById",
            group_id=group_id,
            fields="members_count",
        )
        if isinstance(resp, list) and resp:
            return int(resp[0].get("members_count") or 0)
    except Exception:
        # не критично — просто вернем None
        return None
    return None


def get_recent_posts_stats(group_id: int, count: int = 10) -> List[PostStat]:
    # owner_id для сообществ — отрицательный
    resp = _vk_call(
        "wall.get",
        owner_id=-(group_id),
        count=count,
        extended=0,
    )
    items = resp.get("items", [])
    stats: List[PostStat] = []
    for it in items:
        post_id = int(it.get("id"))
        date = int(it.get("date"))
        text = (it.get("text") or "").strip().replace("\n", " ")
        text_preview = text[:120] + ("…" if len(text) > 120 else "")

        likes = int((it.get("likes") or {}).get("count") or 0)
        comments = int((it.get("comments") or {}).get("count") or 0)
        reposts = int((it.get("reposts") or {}).get("count") or 0)
        views = int((it.get("views") or {}).get("count") or 0)

        stats.append(
            PostStat(
                post_id=post_id,
                date=date,
                text_preview=text_preview,
                likes=likes,
                comments=comments,
                reposts=reposts,
                views=views,
            )
        )
    return stats


def get_summary(group_id: int, last_n: int = 10) -> StatsSummary:
    posts = get_recent_posts_stats(group_id, count=last_n)
    followers = get_group_followers_count(group_id)

    return StatsSummary(
        posts_count=len(posts),
        likes_total=sum(p.likes for p in posts),
        comments_total=sum(p.comments for p in posts),
        reposts_total=sum(p.reposts for p in posts),
        views_total=sum(p.views for p in posts),
        followers=followers,
        posts=posts,
    )

