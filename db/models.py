from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    products: Mapped[list['Product']] = relationship(
        "Product", back_populates='client', cascade='all, delete-orphan'
    )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
    client: Mapped[Client] = relationship('Client', back_populates='products', lazy='selectin')






