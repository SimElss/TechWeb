from datetime import datetime
from sqlalchemy import DateTime, Table, Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between Users and Beers
association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("beer_id", ForeignKey("beers.id", ondelete="CASCADE"), primary_key=True),
)

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    beer_id = Column(Integer, ForeignKey('beers.id', ondelete="SET NULL"))
    quantity = Column(Integer, nullable=False)

    # Relationship with Users and Beers
    user = relationship("Users", back_populates="cart_items")
    beer = relationship("Beers", back_populates="cart_items")

class Beers(Base):
    __tablename__ = 'beers'

    id = Column(String(72), primary_key=True)
    name = Column(String(72))
    brewery = Column(String(72))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String(72))
    image = Column(String(72))
    isdeleted = Column(Boolean, default=False)

    users = relationship(
        "Users",
        secondary=association_table,
        back_populates="beers"
    )
    cart_items = relationship("CartItem", back_populates="beer")
    
class Admins(Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    user: Mapped["Users"] = relationship("Users", back_populates="admin")

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
    admin: Mapped["Admins"] = relationship("Admins", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("Users", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"))
    beer_id = Column(Integer, ForeignKey('beers.id', ondelete="SET NULL"))
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("Order", back_populates="order_items")
    beer = relationship("Beers")
