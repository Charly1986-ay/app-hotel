from enum import Enum
from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

class UnitsType(str, Enum):
    UNITS = 'units'
    LITER = 'liter'
    GRAM = 'gram'
    METRO = 'metro' 

class StatusSupply(str, Enum):
    AVAILABLE = 'available'   
    UNAVAILABLE = 'unavailable'

class Supply(SQLModel, table=True):
    __tablename__ = 'supply'
    __table_args__ = {'extend_existing': True}
    
    id: Optional[int] = Field(default=None, primary_key=True)    
    name: str
    description: str    
    stock: int = Field(default=1, ge=0) 
    stock_min: int = Field(default=1, ge=0)
    price: int = Field(default=0)    
    units_type: UnitsType = Field(default=UnitsType.UNITS)
    status: StatusSupply = Field(default=StatusSupply.AVAILABLE)


class SupplyCreate(SQLModel):
    name: str
    description: str    
    stock: int
    stock_min: int
    price: int
    units_type: UnitsType = UnitsType.UNITS
    status: StatusSupply = StatusSupply.AVAILABLE

class SupplyUpdate(SQLModel):
    name: Optional[str]
    description: Optional[str]
    stock: Optional[int]
    stock_min: Optional[int]
    price: Optional[int]
    units_type: Optional[UnitsType]
    status: Optional[StatusSupply]

class SupplyResponse(SQLModel):
    id: int
    name: str
    description: str    
    stock: int
    stock_min: int
    price: int
    units_type: UnitsType
    status: StatusSupply
    model_config = ConfigDict(from_attributes=True)