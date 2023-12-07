from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from alembic import op
import sqlalchemy as sa


engine = create_engine('postgresql://username:password@localhost/db_name')
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    prices = relationship("Price", back_populates="product")

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Feature(Base):
    __tablename__ = 'feature'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)

class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    type = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", back_populates="prices")


def upgrade():
    op.create_table(
        'product',
        Column('id', sa.Integer(), nullable=False),
        Column('name', sa.String(), nullable=True),
        Column('created_at', sa.DateTime(), nullable=True),
        Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'city',
        Column('id', sa.Integer(), nullable=False),
        Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'category',
        Column('id', sa.Integer(), nullable=False),
        Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'feature',
        Column('id', sa.Integer(), nullable=False),
        Column('name', sa.String(), nullable=True),
        Column('value', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'price',
        Column('id', sa.Integer(), nullable=False),
        Column('price', sa.Integer(), nullable=True),
        Column('type', sa.String(), nullable=True),
        Column('url', sa.String(), nullable=True),
        Column('created_at', sa.DateTime(), nullable=True),
        Column('updated_at', sa.DateTime(), nullable=True),
        Column('product_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['product.id']),
        sa.PrimaryKeyConstraint('id')
    )


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    upgrade()

    products = session.query(Product).join(Price).group_by(Product.id).order_by(Product.updated_at.desc()).all()

    for product in products:
        latest_price = session.query(Price).filter(Price.product_id == product.id).order_by(
            Price.updated_at.desc()).first()
        print(f"Товар: {product.name}, Новейшая цена: {latest_price.price}")

    session.close()
