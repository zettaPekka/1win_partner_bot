from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import BigInteger


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    next_k: Mapped[float] = mapped_column(nullable=True)
    gambling_id: Mapped[str] = mapped_column(nullable=True)


class GamblingData(Base):
    __tablename__ = 'gambling_data'
    
    user_id: Mapped[str] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)