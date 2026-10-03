"""
Демонстраційний скрипт для лабораторної з контейнеризації.

Мета: показати, що "свій" контейнер (з кодом проєкту) бачить "чужий"
контейнер БД по мережі Docker, вміє туди щось ЗАПИСАТИ і потім це
ПРОЧИТАТИ, і що результат видно в логах — як docker logs, так і у
файлі на хост-машині (через змонтований том), який переживе
видалення контейнера.

Навмисно взято один із доменних класів проєкту (Episode-подібна
структура з полями episode_id/title/description), щоб "код" у
контейнері був не абстрактним hello-world, а реально пов'язаним із
курсовою роботою.
"""

import logging
import os
import sys
import time
from dataclasses import dataclass

import psycopg2

# ---------------------------------------------------------------------------
# 1. Налаштування логування: одночасно в stdout (видно через `docker logs`)
#    і у файл /app/logs/app.log, який монтується як volume з хост-машини,
#    тому переживе `docker rm` контейнера.
# ---------------------------------------------------------------------------
LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),      # -> docker logs
        logging.FileHandler(LOG_FILE, mode="a"),  # -> файл на хості
    ],
)
log = logging.getLogger("docker-lab-demo")


# ---------------------------------------------------------------------------
# 2. Мінімальна доменна модель (спрощений аналог domain.models.Episode)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class EpisodeRecord:
    episode_id: str
    title: str
    description: str


DEMO_EPISODE = EpisodeRecord(
    episode_id="ep-docker-lab-001",
    title="Docker Lab Demo Episode",
    description="Цей запис створено автоматично з контейнера podcast-app "
                 "для перевірки з'єднання з контейнером БД.",
)


# ---------------------------------------------------------------------------
# 3. Параметри підключення — читаються зі змінних оточення
#    (передаються через `docker run -e ...` або docker-compose.yml)
# ---------------------------------------------------------------------------
DB_HOST = os.environ.get("DB_HOST", "podcast-db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "podcast_demo")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

MAX_RETRIES = 15
RETRY_DELAY_SEC = 2


def wait_for_db() -> psycopg2.extensions.connection:
    """БД-контейнер може стартувати повільніше за app-контейнер, тому
    підключаємось з ретраями, а не падаємо одразу."""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info(f"Спроба підключення до БД {DB_HOST}:{DB_PORT} "
                      f"(спроба {attempt}/{MAX_RETRIES})...")
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=5,
            )
            log.info("Підключення до БД успішне.")
            return conn
        except psycopg2.OperationalError as exc:
            last_error = exc
            log.warning(f"БД ще не готова: {exc}")
            time.sleep(RETRY_DELAY_SEC)
    log.error("Не вдалося підключитися до БД після всіх спроб.")
    raise SystemExit(1) from last_error


def ensure_table(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS episodes_demo (
                episode_id  TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at  TIMESTAMP DEFAULT NOW()
            );
            """
        )
    conn.commit()
    log.info("Таблицю 'episodes_demo' перевірено/створено.")


def write_episode(conn, episode: EpisodeRecord) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO episodes_demo (episode_id, title, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (episode_id) DO UPDATE
                SET title = EXCLUDED.title,
                    description = EXCLUDED.description;
            """,
            (episode.episode_id, episode.title, episode.description),
        )
    conn.commit()
    log.info(f"Записано епізод у БД: {episode.episode_id!r}")


def read_all_episodes(conn) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT episode_id, title, description, created_at "
            "FROM episodes_demo ORDER BY created_at;"
        )
        rows = cur.fetchall()
    return rows


def main() -> None:
    log.info("=== Старт демо-застосунку контейнеризації ===")
    conn = wait_for_db()
    try:
        ensure_table(conn)
        write_episode(conn, DEMO_EPISODE)

        rows = read_all_episodes(conn)
        log.info(f"Прочитано {len(rows)} рядків з таблиці 'episodes_demo':")
        for episode_id, title, description, created_at in rows:
            log.info(
                f"  -> id={episode_id} | title={title!r} | "
                f"created_at={created_at} | description={description!r}"
            )
        log.info("=== Успішне завершення: запис і читання підтверджено ===")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
