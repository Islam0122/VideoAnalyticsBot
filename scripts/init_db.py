import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.database import init_db_sync
from src.config import config


def main():
    print("Инициализация базы данных...")
    print(f"URL: {config.DATABASE_URL}")

    try:
        init_db_sync()
        print("✅ База данных успешно инициализирована!")
        print("\nСозданные таблицы:")
        print("  - videos")
        print("  - video_snapshots")
        print("\nТеперь можете загрузить данные командой:")
        print("  python scripts/load_data.py data/videos.json")

    except Exception as e:
        print(f"❌ Ошибка при инициализации БД: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()