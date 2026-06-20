from enum import Enum
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

class UnitsType(str, Enum):
    UNITS = 'units'
    LITER = 'liter'
    GRAM = 'gram'
    METRO = 'metro' 

class StatusArticle(str, Enum):
    AVAILABLE = 'available'   
    UNAVAILABLE = 'unavailable'

class Article(SQLModel, table=True):
    __tablename__ = 'article'
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)    
    name: str
    description: str    
    stock: int = Field(default=1, ge=0) 
    price: int = Field(default=0)    
    units_type: UnitsType = Field(default=UnitsType.UNITS)
    status: StatusArticle = Field(default=StatusArticle.AVAILABLE)


class ArticleCreate(SQLModel):
    name: str
    description: str    
    stock: int
    price: int
    units_type: UnitsType = UnitsType.UNITS
    status: StatusArticle = StatusArticle.AVAILABLE

class ArticleUpdate(SQLModel):
    name: Optional[str]
    description: Optional[str]
    stock: Optional[int]
    price: Optional[int]
    units_type: Optional[UnitsType]
    status: Optional[StatusArticle]

class ArticleResponse(SQLModel):
    id: int
    name: str
    description: str    
    stock: int
    price: int
    units_type: UnitsType
    status: StatusArticle
    model_config = ConfigDict(from_attributes=True)