from sqlalchemy import Column, ForeignKey, String, Boolean, Table, Float
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
        "beer_id",
        ForeignKey("beers.id"),
        primary_key=True
    ),
)

class Beers(Base):
    __tablename__= 'beers'

    id: Mapped[str] = mapped_column(String(72), primary_key=True)
    name: Mapped[str] = mapped_column(String(72))
    Author: Mapped[str] = mapped_column(String(72))
    Editor: Mapped[Optional[str]] = mapped_column(String(72), nullable=True)
    price: Mapped[float] = mapped_column(Float(72))
    bought: Mapped[bool] = mapped_column(Boolean)
    new_owner_id: Mapped[Optional[str]] = mapped_column(String(72), nullable=True)

    user:  Mapped[List["Users"]] = relationship(
        secondary = association_table, back_populates="beer"
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

    beer: Mapped[List["Beers"]] = relationship(
        secondary = association_table, back_populates="user"
    )
    admin: Mapped[List["Admins"]] = relationship()


