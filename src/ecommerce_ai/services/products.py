from ecommerce_ai.repositories.product_repository import ProductRepository
from ecommerce_ai.schemas.products import (
    ProductSearchRequest,
    ProductSearchResult,
)


class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def search_products(
        self,
        request: ProductSearchRequest,
    ) -> list[ProductSearchResult]:

        rows = await self.repository.search_products(request)

        results = []

        for product, variant in rows:

            results.append(
                ProductSearchResult(
                    product_id=product.id,
                    name=product.name,
                    brand=product.brand,
                    description=product.description,
                    rating=product.rating,

                    variant_id=variant.id,
                    sku=variant.sku,
                    variant_name=variant.name,

                    price=variant.price,
                    discount=variant.discount,
                    stock_quantity=variant.stock_quantity,
                    is_active=variant.is_active,

                    specifications=variant.specifications or {},
                )
            )

        return results