from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ecommerce_ai.models.product import Product, ProductVariant
from ecommerce_ai.schemas.products import ProductSearchRequest


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_products(
        self,
        request: ProductSearchRequest,
    ) -> list[tuple[Product, ProductVariant]]:

        stmt = (
            select(Product,ProductVariant)
            .join(
                ProductVariant,
                ProductVariant.product_id == Product.id,
            )
        )

        # -------------------------
        # Text search
        # -------------------------

        if request.query:
            search_pattern = f"%{request.query}%"

            stmt = stmt.where(
                Product.name.ilike(search_pattern)
                | Product.description.ilike(search_pattern)
                | Product.brand.ilike(search_pattern)
            )

        # -------------------------
        # Brand filter
        # -------------------------

        if request.brand:
            stmt = stmt.where(
                Product.brand.ilike(f"%{request.brand}%")
            )

        # -------------------------
        # Minimum price
        # -------------------------

        if request.min_price is not None:
            stmt = stmt.where(
                ProductVariant.price >= request.min_price
            )

        # -------------------------
        # Maximum price
        # -------------------------

        if request.max_price is not None:
            stmt = stmt.where(
                ProductVariant.price <= request.max_price
            )

        # -------------------------
        # Availability
        # -------------------------

        if request.available_only:
            stmt = stmt.where(
                ProductVariant.stock_quantity > 0,
                ProductVariant.is_active.is_(True),
            )

        # -------------------------
        # Limit
        # -------------------------

        stmt = stmt.limit(request.limit)

        result = await self.session.execute(stmt)

        rows = result.all()

        return rows