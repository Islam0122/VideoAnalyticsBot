import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.loader import load_json_to_db, clear_db
from src.config import config


def main():
    if len(sys.argv) < 2:
        print("Использование: python scripts/load_data.py <путь_к_json_файлу>")
        print("Пример: python scripts/load_data.py data/videos.json")
        sys.exit(1)

    json_path = sys.argv[1]

    if not Path(json_path).exists():
        print(f"❌ Файл не найден: {json_path}")
        sys.exit(1)

    print("⚠️  Внимание! Этот скрипт загрузит данные в базу.")
    response = input("Очистить существующие данные перед загрузкой? (y/N): ")

    try:
        if response.lower() == 'y':
            clear_db()

        load_json_to_db(json_path)
        print("\n✅ Данные успешно загружены!")
        print("\nТеперь можете запустить бота:")
        print("  python main.py")

    except Exception as e:
        print(f"\n❌ Ошибка при загрузке данных: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()