from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username = Column(String, unique=True, index=True)

    context: Mapped[List["UserContext"]] = relationship(back_populates="user")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username})"


class UserContext(Base):
    __tablename__ = "users_context"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user: Mapped["User"] = relationship(back_populates="context")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    is_from_user: Mapped[bool] = mapped_column(Boolean)
    message_text: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return (f"History("
                f"user_id={self.user_id}, "
                f"is_from_user={self.is_from_user}, "
                f"message_text={self.message_text[:20]}..."
                f")")

