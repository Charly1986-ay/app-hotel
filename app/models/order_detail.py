from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from app.models.article import Article
from app.models.order import Order


class OrderDetail(SQLModel, table=True):
    __tablename__ = 'order_detail'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    article_id: int = Field(foreign_key="article.id")
    quantity: int = Field(default=1, ge=1)  # Cuánto pide el supervisor

    # Relaciones
    order: "Order" = Relationship(back_populates="details")
    article: "Article" = Relationship()


class OrderDetailCreate(SQLModel):
    order_id: int
    article_id: int
    quantity: int

class OrderDetailResponse(SQLModel):
    id: int
    order_id: int
    article_id: int
    quantity: int
    model_config = ConfigDict(from_attributes=True)