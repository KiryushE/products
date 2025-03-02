from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from datetime import datetime

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    products: Mapped[list['Product']] = relationship(
        "Product", back_populates='client', cascade='all, delete-orphan'
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    client_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clients.id"), nullable=False
    )
    client: Mapped[Client] = relationship(
        "Client", back_populates="products", lazy="selectin"
    )
    product_users: Mapped[list['SavedProduct']] = relationship(
        'SavedProduct', back_populates='product'
    )


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_products: Mapped[list['SavedProduct']] = relationship(
        'SavedProduct', back_populates='user'
    )


class SavedProduct(Base):
    __tablename__ = "saved_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), nullable=False
    )
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    in_shopping_cart: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship("User", back_populates="user_products")
    product: Mapped[Product] = relationship("Product", back_populates="product_users")

    __table_args__ = (
       UniqueConstraint('user_id', 'product_id', name='unique_user_product'),
    )


