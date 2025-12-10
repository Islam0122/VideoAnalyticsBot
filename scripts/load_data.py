import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.loader import load_json_to_db, clear_db

def main():
    if len(sys.argv) < 2:
        print("Использование: python scripts/load_data.py <путь_к_json_файлу> [--yes]")
        sys.exit(1)

    json_path = sys.argv[1]
    auto_confirm = "--yes" in sys.argv

    if not Path(json_path).exists():
        print(f"❌ Файл не найден: {json_path}")
        sys.exit(1)

    print("⚠️ Внимание! Этот скрипт загрузит данные в базу.")

    if auto_confirm:
        clear_db()

    load_json_to_db(json_path)
    print("✅ Данные успешно загружены!")

if __name__ == "__main__":
    main()
