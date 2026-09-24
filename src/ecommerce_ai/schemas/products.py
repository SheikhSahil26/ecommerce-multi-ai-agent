from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field


class ProductSearchRequest(BaseModel):
    query: str | None = None
    category: str | None = None
    brand: str | None = None

    min_price: Decimal | None = None
    max_price: Decimal | None = None

    specifications: dict[str, Any] = Field(
        default_factory=dict
    )

    available_only: bool = True

    limit: int = Field(
        default=10,
        ge=1,
        le=50,
    )


class ProductVariantResult(BaseModel):
    id: int
    sku: str
    name: str
    price: Decimal
    discount: Decimal
    stock_quantity: int
    is_active: bool


class ProductResult(BaseModel):
    id: int
    name: str
    brand: str | None
    description: str | None
    rating: float | None
    specifications: dict | None


class ProductSearchResult(BaseModel):
    product_id: int
    name: str
    brand: str | None
    description: str | None
    rating: float | None

    variant_id: int
    sku: str
    variant_name: str | None

    price: Decimal
    discount: Decimal
    stock_quantity: int
    is_active: bool

    specifications: dict