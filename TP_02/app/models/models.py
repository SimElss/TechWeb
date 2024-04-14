from sqlalchemy import Column, ForeignKey, String, Boolean, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from ..database import Base 


association_table = Table(
    "association_table",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True
    ),
    Column(
        "book_id",
        ForeignKey("books.id"),
        primary_key=True
),
)

class Books(Base):
    __tablename__= 'books'

    id: Mapped[str] = mapped_column(String(72), primary_key=True)
    title: Mapped[str] = mapped_column(String(72))
    Author: Mapped[str] = mapped_column(String(72))
    Editor: Mapped[Optional[str]] = mapped_column(String(72), nullable=True)
    
    user:  Mapped[List["Users"]] = relationship(
        secondary = association_table, back_populates="book"
    )


class Admins(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["Users"] = relationship()

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(72), primary_key=True) #primary key and indexable
    username: Mapped[str] = mapped_column(String(72), unique=True) #unique but cannot be the primary key as the id is
    name: Mapped[str] = mapped_column(String(72))
    surname: Mapped[str] = mapped_column(String(72))
    password: Mapped[str] = mapped_column(String(72))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    group: Mapped[str] = mapped_column(String(7))
    whitelist: Mapped[bool] = mapped_column(Boolean)

    admin: Mapped[List["Admins"]] = relationship()
    book: Mapped[List["Books"]] = relationship(
        secondary = association_table, back_populates="user"
    )


