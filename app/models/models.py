from sqlalchemy import Table, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("beer_id", ForeignKey("beers.id"), primary_key=True),
)


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    beer_id = Column(Integer, ForeignKey('beers.id'))

    # Relationship with Users and Beers
    user = relationship("Users", back_populates="cart_items")
    beer = relationship("Beers", back_populates="cart_items")
    

class Beers(Base):
    __tablename__ = 'beers'
    id: Mapped[str] = mapped_column(String(72), primary_key=True)
    name: Mapped[str] = mapped_column(String(72))
    brewery: Mapped[str] = mapped_column(String(72))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(72))
    image: Mapped[str] = mapped_column(String(72))

    users: Mapped[list["Users"]] = relationship(
        secondary=association_table, back_populates="beers"
    )
    cart_items = relationship("CartItem", back_populates="beer")

class Admins(Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["Users"] = relationship()

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String(72), primary_key=True)
    username: Mapped[str] = mapped_column(String(72), unique=True)
    name: Mapped[str] = mapped_column(String(72))
    surname: Mapped[str] = mapped_column(String(72))
    password: Mapped[str] = mapped_column(String(72))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    group: Mapped[str] = mapped_column(String(7))
    whitelist: Mapped[bool] = mapped_column(Boolean)

    beers: Mapped[list["Beers"]] = relationship(
        secondary=association_table, back_populates="users"
    )
    admin: Mapped["Admins"] = relationship()
    cart_items = relationship("CartItem", back_populates="user")

