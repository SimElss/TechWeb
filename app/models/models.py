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
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="beer")

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
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False)

class Cart(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["Users"] = relationship("Users", back_populates="cart")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = 'cart_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    beer_id: Mapped[str] = mapped_column(ForeignKey("beers.id"))
    quantity: Mapped[int] = mapped_column(Integer)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
    beer: Mapped["Beers"] = relationship("Beers", back_populates="cart_items")
