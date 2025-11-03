from src.generators.text_gen import PostGenerator
from src.generators.image_gen import ImageGenerator
from src.social_publishers.vk_publisher import VKPublisher
from src.config import VK_GROUP_ID
from src.social_stats.vk_stats import get_summary


def main():
    TOPIC = "Жизнь в ритме ИИ: как технологии становятся продолжением нашего мышления и чувств"
    TONE = "философский, мягкий, вдумчивый"

    # 1) Генерируем текст поста
    post = PostGenerator().generate_post(topic=TOPIC, tone=TONE)

    print("=== TITLE ===")
    print(post.title)
    print("\n=== TEXT ===")
    print(post.text)
    print("\n=== IMAGE PROMPT ===")
    print(post.image_prompt)
    print("\n=== HASHTAGS ===")
    print(" ".join(post.hashtags))

    # 2) Генерируем изображение
    img = ImageGenerator().generate_image(prompt=post.image_prompt, size="1024x1024")
    print(f"\n=== IMAGE SAVED === {img.path}")

    # 3) Публикуем в VK
    publisher = VKPublisher()
    result = publisher.publish_post(
        text=f"{post.title}\n\n{post.text}\n\n{' '.join(post.hashtags)}",
        image_path=img.path,
    )
    print(f"\n=== VK POSTED === https://vk.com/wall{result.full_id}")

    # 4) Показываем статистику
    summary = get_summary(last_n=10, group_id=VK_GROUP_ID)
    print("\n=== STATS (last 10 posts) ===")
    print(f"followers: {summary.followers}")
    print(f"posts_count: {summary.posts_count}")
    print(f"likes_total: {summary.likes_total} | comments_total: {summary.comments_total} | "
          f"reposts_total: {summary.reposts_total} | views_total: {summary.views_total}")

    print("\n# posts breakdown:")
    for p in summary.posts:
        print(f"- id={p.post_id} likes={p.likes} comments={p.comments} reposts={p.reposts} views={p.views} | {p.text_preview}")


if __name__ == "__main__":
    main()
