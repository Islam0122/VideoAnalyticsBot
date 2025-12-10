from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
import uuid


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "videos"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    video_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    views_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    reports_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow,
                                                 onupdate=datetime.utcnow)

    snapshots: Mapped[List["VideoSnapshot"]] = relationship(
        "VideoSnapshot", back_populates="video", cascade="all, delete-orphan"
    )


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"),
                                                nullable=False, index=True)
    views_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    reports_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    delta_views_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    delta_likes_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    delta_comments_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    delta_reports_count: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    video: Mapped["Video"] = relationship("Video", back_populates="snapshots")
