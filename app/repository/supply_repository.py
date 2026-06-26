from sqlmodel import select

from app.models.supply import Supply

from sqlmodel.ext.asyncio.session import AsyncSession

class SupplyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, supply_id: int) -> Supply | None:
        return await self.db.get(Supply, supply_id)
    
    async def get_all(self) -> list[Supply]:
        result =  await self.db.exec(select(Supply))
        return result.all()
    
    async def get_insufficient_stock(self) -> list[Supply]:
        result = await self.db.exec(
            select(Supply).where(
                Supply.stock <= Supply.stock_min
                )
            )        
        return result.all()
    
    async def create(self, supply: Supply) -> Supply:
        self.db.add(supply)
        await self.db.commit()
        await self.db.refresh(supply)
        return supply

    async def update(self, supply: Supply, updates: dict) -> Supply:        
        for key, value in updates.items():
            setattr(supply, key, value)

        self.db.add(supply)
        await self.db.commit()
        await self.db.refresh(supply)
        return supply