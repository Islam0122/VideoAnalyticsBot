import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.database.models import Video, VideoSnapshot
from src.database.database import sync_engine
from typing import Optional



def load_json_to_db(json_path: str, batch_size: int = 100):
    print(f"Загрузка данных из {json_path}...")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    videos_data = data.get('videos', [])
    print(f"Найдено {len(videos_data)} видео")

    video_count = 0
    snapshot_count = 0

    try:
        with Session(sync_engine) as session:
            for i, video_data in enumerate(videos_data, start=1):
                video = Video(
                    id=video_data['id'],
                    creator_id=video_data['creator_id'],
                    video_created_at=video_data.get('video_created_at'),
                    views_count=int(video_data.get('views_count') or 0),
                    likes_count=int(video_data.get('likes_count') or 0),
                    comments_count=int(video_data.get('comments_count') or 0),
                    reports_count=int(video_data.get('reports_count') or 0),
                    created_at=video_data.get('created_at'),
                    updated_at=video_data.get('updated_at')
                )
                session.add(video)
                video_count += 1

                for snapshot_data in video_data.get('snapshots', []):
                    snapshot = VideoSnapshot(
                        id=snapshot_data['id'],
                        video_id=video.id,
                        views_count=int(snapshot_data.get('views_count') or 0),
                        likes_count=int(snapshot_data.get('likes_count') or 0),
                        comments_count=int(snapshot_data.get('comments_count') or 0),
                        reports_count=int(snapshot_data.get('reports_count') or 0),
                        delta_views_count=int(snapshot_data.get('delta_views_count') or 0),
                        delta_likes_count=int(snapshot_data.get('delta_likes_count') or 0),
                        delta_comments_count=int(snapshot_data.get('delta_comments_count') or 0),
                        delta_reports_count=int(snapshot_data.get('delta_reports_count') or 0),
                        created_at=snapshot_data.get('created_at'),
                        updated_at=snapshot_data.get('updated_at')
                    )
                    session.add(snapshot)
                    snapshot_count += 1

                if i % batch_size == 0:
                    session.commit()
                    print(f"[INFO] Загружено {i} видео...")

            session.commit()
            print(f"\n[INFO] Загрузка завершена успешно!")
            print(f"  - Видео: {video_count}")
            print(f"  - Снапшотов: {snapshot_count}")

    except SQLAlchemyError as e:
        print(f"[ERROR] Ошибка при работе с базой: {e}")


def clear_db():
    print("Очистка базы данных...")
    try:
        with Session(sync_engine) as session:
            session.query(VideoSnapshot).delete()
            session.query(Video).delete()
            session.commit()
        print("База данных успешно очищена")
    except SQLAlchemyError as e:
        print(f"[ERROR] Не удалось очистить базу: {e}")
