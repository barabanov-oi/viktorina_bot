from app.common.utils import stable_hash, utcnow
from app.domain.enums import Difficulty
from app.persistence.db import SessionLocal
from app.persistence.models import Topic, Question


TOPICS = [
    ("history", "История"),
    ("science", "Наука"),
    ("movies", "Кино"),
    ("sport", "Спорт"),
]


def make_question(topic_id: int, i: int) -> Question:
    text = f"Тестовый вопрос #{i} для topic={topic_id}?"
    options = [f"Вариант {n}" for n in range(1, 5)]
    payload = {"text": text, "options": options}
    return Question(
        topic_id=topic_id,
        language="ru",
        difficulty=Difficulty.easy,
        text=text,
        options=options,
        correct_index=i % 4,
        explanation="Потому что это seed.",
        tags=["seed"],
        source="bank",
        content_hash=stable_hash(payload),
        created_at=utcnow(),
        is_active=True,
    )


def main() -> None:
    with SessionLocal() as session:
        existing = {t.slug: t for t in session.query(Topic).all()}
        for slug, title in TOPICS:
            if slug not in existing:
                session.add(Topic(slug=slug, title=title, description=title, language="ru", is_active=True))
        session.commit()

        topics = session.query(Topic).all()
        current_count = session.query(Question).count()
        if current_count >= 20:
            print("Seed пропущен: вопросов уже достаточно")
            return

        idx = 0
        while session.query(Question).count() < 20:
            topic = topics[idx % len(topics)]
            q = make_question(topic.id, idx + 1)
            if not session.query(Question).filter_by(content_hash=q.content_hash).first():
                session.add(q)
                session.commit()
            idx += 1
        print("Seed завершен")


if __name__ == "__main__":
    main()
