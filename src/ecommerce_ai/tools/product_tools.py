from langchain_core.tools import tool

from ecommerce_ai.repositories.product_repository import ProductRepository
from ecommerce_ai.schemas.products import ProductSearchRequest
from ecommerce_ai.services.products import ProductService


def create_product_tools(repository: ProductRepository):

    @tool
    async def search_products(request: ProductSearchRequest):
        """
        Search the e-commerce product catalog.

        Use this tool when the user wants to:
        - find products
        - filter products by brand
        - filter products by price
        - find available products
        - search using product specifications

        The tool searches the actual product database and returns
        matching products with their variants, prices, discounts,
        stock quantities, and specifications.

        Do not invent product information when the tool can provide it.
        """

        service = ProductService(repository)

        products = await service.search_products(request)

        return products

    return [search_products]