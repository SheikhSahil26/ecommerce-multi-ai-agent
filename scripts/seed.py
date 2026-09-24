import asyncio
from decimal import Decimal

from sqlalchemy import delete

from ecommerce_ai.db.database import AsyncSessionLocal
from ecommerce_ai.models.product import Category, Product, ProductVariant


async def seed_database():
    async with AsyncSessionLocal() as session:

        # --------------------------------------------------
        # 1. Clear existing product data
        # --------------------------------------------------

        await session.execute(delete(ProductVariant))
        await session.execute(delete(Product))
        await session.execute(delete(Category))

        # --------------------------------------------------
        # 2. Categories
        # --------------------------------------------------

        laptops = Category(
            name="Laptops",
            slug="laptops",
            description="Laptops for work, gaming, programming and everyday use.",
        )

        phones = Category(
            name="Smartphones",
            slug="smartphones",
            description="Smartphones from different brands and price ranges.",
        )

        headphones = Category(
            name="Headphones",
            slug="headphones",
            description="Wireless and wired headphones and earphones.",
        )

        monitors = Category(
            name="Monitors",
            slug="monitors",
            description="Monitors for gaming, productivity and professional work.",
        )

        session.add_all([
            laptops,
            phones,
            headphones,
            monitors,
        ])

        await session.flush()

        # --------------------------------------------------
        # 3. Products
        # --------------------------------------------------

        products = [
            Product(
                category_id=laptops.id,
                name="Lenovo Legion 5",
                description=(
                    "Gaming laptop with powerful processor and dedicated GPU. "
                    "Suitable for gaming, programming and heavy workloads."
                ),
                brand="Lenovo",
                rating=4.6,
                specifications={
                    "processor": "AMD Ryzen 7 7840HS",
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "gpu": "NVIDIA RTX 4060",
                    "display": "15.6 inch",
                },
            ),

            Product(
                category_id=laptops.id,
                name="ASUS TUF Gaming F15",
                description=(
                    "Gaming laptop designed for high-performance gaming "
                    "and demanding development workloads."
                ),
                brand="ASUS",
                rating=4.5,
                specifications={
                    "processor": "Intel Core i7-12700H",
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "gpu": "NVIDIA RTX 3050",
                    "display": "15.6 inch",
                },
            ),

            Product(
                category_id=laptops.id,
                name="Apple MacBook Air M3",
                description=(
                    "Thin and lightweight laptop with Apple M3 chip. "
                    "Suitable for development, productivity and creative work."
                ),
                brand="Apple",
                rating=4.8,
                specifications={
                    "processor": "Apple M3",
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "gpu": "Integrated",
                    "display": "13.6 inch",
                },
            ),

            Product(
                category_id=laptops.id,
                name="HP Pavilion 15",
                description=(
                    "Everyday laptop for students, office work, programming "
                    "and general productivity."
                ),
                brand="HP",
                rating=4.2,
                specifications={
                    "processor": "Intel Core i5-1335U",
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "gpu": "Integrated",
                    "display": "15.6 inch",
                },
            ),

            Product(
                category_id=laptops.id,
                name="Dell Inspiron 14",
                description=(
                    "Compact productivity laptop suitable for students "
                    "and professionals."
                ),
                brand="Dell",
                rating=4.3,
                specifications={
                    "processor": "Intel Core i5-1335U",
                    "ram": "8GB",
                    "storage": "512GB SSD",
                    "gpu": "Integrated",
                    "display": "14 inch",
                },
            ),

            Product(
                category_id=phones.id,
                name="Samsung Galaxy S25",
                description=(
                    "Premium Android smartphone with high-performance processor "
                    "and advanced camera system."
                ),
                brand="Samsung",
                rating=4.7,
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "camera": "50MP",
                    "battery": "4000mAh",
                    "display": "6.2 inch AMOLED",
                },
            ),

            Product(
                category_id=phones.id,
                name="Google Pixel 9",
                description=(
                    "Google smartphone with excellent computational photography "
                    "and clean Android experience."
                ),
                brand="Google",
                rating=4.6,
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "camera": "50MP",
                    "battery": "4700mAh",
                    "display": "6.3 inch OLED",
                },
            ),

            Product(
                category_id=phones.id,
                name="OnePlus 13",
                description=(
                    "High-performance Android smartphone with large battery "
                    "and fast charging."
                ),
                brand="OnePlus",
                rating=4.5,
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "camera": "50MP",
                    "battery": "6000mAh",
                    "display": "6.82 inch AMOLED",
                },
            ),

            Product(
                category_id=headphones.id,
                name="Sony WH-1000XM5",
                description=(
                    "Premium wireless noise-cancelling headphones "
                    "with excellent sound quality."
                ),
                brand="Sony",
                rating=4.8,
                specifications={
                    "type": "Over-ear",
                    "connectivity": "Bluetooth",
                    "noise_cancellation": "Active",
                    "battery": "30 hours",
                },
            ),

            Product(
                category_id=headphones.id,
                name="Bose QuietComfort Ultra",
                description=(
                    "Premium wireless headphones with advanced noise cancellation "
                    "and immersive audio."
                ),
                brand="Bose",
                rating=4.7,
                specifications={
                    "type": "Over-ear",
                    "connectivity": "Bluetooth",
                    "noise_cancellation": "Active",
                    "battery": "24 hours",
                },
            ),

            Product(
                category_id=monitors.id,
                name="LG UltraGear 27",
                description=(
                    "Gaming monitor with high refresh rate and fast response time."
                ),
                brand="LG",
                rating=4.5,
                specifications={
                    "size": "27 inch",
                    "resolution": "2560x1440",
                    "refresh_rate": "165Hz",
                    "panel": "IPS",
                },
            ),

            Product(
                category_id=monitors.id,
                name="Dell UltraSharp 27",
                description=(
                    "Professional monitor designed for productivity, "
                    "software development and creative workloads."
                ),
                brand="Dell",
                rating=4.6,
                specifications={
                    "size": "27 inch",
                    "resolution": "2560x1440",
                    "refresh_rate": "60Hz",
                    "panel": "IPS",
                },
            ),
        ]

        session.add_all(products)

        await session.flush()

        # --------------------------------------------------
        # 4. Product Variants
        # --------------------------------------------------

        variants = [
            # -------------------------
            # Lenovo Legion 5
            # -------------------------

            ProductVariant(
                product_id=products[0].id,
                sku="LEGION5-R7-16-512",
                name="Ryzen 7 / 16GB / 512GB",
                price=Decimal("69999.00"),
                discount=Decimal("5000.00"),
                stock_quantity=12,
                specifications={
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "color": "Storm Grey",
                },
                is_active=True,
            ),

            ProductVariant(
                product_id=products[0].id,
                sku="LEGION5-R7-32-1TB",
                name="Ryzen 7 / 32GB / 1TB",
                price=Decimal("84999.00"),
                discount=Decimal("7000.00"),
                stock_quantity=5,
                specifications={
                    "ram": "32GB",
                    "storage": "1TB SSD",
                    "color": "Storm Grey",
                },
                is_active=True,
            ),

            # -------------------------
            # ASUS TUF
            # -------------------------

            ProductVariant(
                product_id=products[1].id,
                sku="TUF-F15-I7-16-512",
                name="Core i7 / 16GB / 512GB",
                price=Decimal("67999.00"),
                discount=Decimal("4000.00"),
                stock_quantity=8,
                specifications={
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "color": "Graphite Black",
                },
                is_active=True,
            ),

            ProductVariant(
                product_id=products[1].id,
                sku="TUF-F15-I7-16-1TB",
                name="Core i7 / 16GB / 1TB",
                price=Decimal("74999.00"),
                discount=Decimal("5000.00"),
                stock_quantity=0,
                specifications={
                    "ram": "16GB",
                    "storage": "1TB SSD",
                    "color": "Graphite Black",
                },
                is_active=True,
            ),

            # -------------------------
            # MacBook
            # -------------------------

            ProductVariant(
                product_id=products[2].id,
                sku="MBA-M3-16-512",
                name="M3 / 16GB / 512GB",
                price=Decimal("109999.00"),
                discount=Decimal("10000.00"),
                stock_quantity=7,
                specifications={
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "color": "Midnight",
                },
                is_active=True,
            ),

            # -------------------------
            # HP Pavilion
            # -------------------------

            ProductVariant(
                product_id=products[3].id,
                sku="HP-PAV-I5-16-512",
                name="Core i5 / 16GB / 512GB",
                price=Decimal("58999.00"),
                discount=Decimal("3000.00"),
                stock_quantity=15,
                specifications={
                    "ram": "16GB",
                    "storage": "512GB SSD",
                    "color": "Silver",
                },
                is_active=True,
            ),

            # -------------------------
            # Dell Inspiron
            # -------------------------

            ProductVariant(
                product_id=products[4].id,
                sku="DELL-INSP-I5-8-512",
                name="Core i5 / 8GB / 512GB",
                price=Decimal("52999.00"),
                discount=Decimal("2500.00"),
                stock_quantity=10,
                specifications={
                    "ram": "8GB",
                    "storage": "512GB SSD",
                    "color": "Platinum Silver",
                },
                is_active=True,
            ),

            # -------------------------
            # Samsung
            # -------------------------

            ProductVariant(
                product_id=products[5].id,
                sku="S25-12-256",
                name="12GB / 256GB",
                price=Decimal("74999.00"),
                discount=Decimal("5000.00"),
                stock_quantity=20,
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "color": "Navy",
                },
                is_active=True,
            ),

            # -------------------------
            # Pixel
            # -------------------------

            ProductVariant(
                product_id=products[6].id,
                sku="PIXEL9-12-256",
                name="12GB / 256GB",
                price=Decimal("69999.00"),
                discount=Decimal("4000.00"),
                stock_quantity=6,
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "color": "Obsidian",
                },
                is_active=True,
            ),

            # -------------------------
            # OnePlus
            # -------------------------

            ProductVariant(
                product_id=products[7].id,
                sku="OP13-12-256",
                name="12GB / 256GB",
                price=Decimal("64999.00"),
                discount=Decimal("6000.00"),
                stock_quantity=0,
                specifications={
                    "ram": "12GB",
                    "storage": "256GB",
                    "color": "Black",
                },
                is_active=True,
            ),

            # -------------------------
            # Sony
            # -------------------------

            ProductVariant(
                product_id=products[8].id,
                sku="SONY-XM5-BLK",
                name="Black",
                price=Decimal("29999.00"),
                discount=Decimal("3000.00"),
                stock_quantity=10,
                specifications={
                    "color": "Black",
                    "connectivity": "Bluetooth",
                },
                is_active=True,
            ),

            ProductVariant(
                product_id=products[8].id,
                sku="SONY-XM5-SLV",
                name="Silver",
                price=Decimal("30999.00"),
                discount=Decimal("3000.00"),
                stock_quantity=0,
                specifications={
                    "color": "Silver",
                    "connectivity": "Bluetooth",
                },
                is_active=True,
            ),

            # -------------------------
            # Bose
            # -------------------------

            ProductVariant(
                product_id=products[9].id,
                sku="BOSE-QCU-BLK",
                name="Black",
                price=Decimal("34999.00"),
                discount=Decimal("4000.00"),
                stock_quantity=4,
                specifications={
                    "color": "Black",
                    "connectivity": "Bluetooth",
                },
                is_active=True,
            ),

            # -------------------------
            # LG Monitor
            # -------------------------

            ProductVariant(
                product_id=products[10].id,
                sku="LG-27-QHD-165",
                name="27 inch / QHD / 165Hz",
                price=Decimal("27999.00"),
                discount=Decimal("2000.00"),
                stock_quantity=9,
                specifications={
                    "size": "27 inch",
                    "resolution": "2560x1440",
                    "refresh_rate": "165Hz",
                },
                is_active=True,
            ),

            # -------------------------
            # Dell Monitor
            # -------------------------

            ProductVariant(
                product_id=products[11].id,
                sku="DELL-US27-QHD",
                name="27 inch / QHD / 60Hz",
                price=Decimal("31999.00"),
                discount=Decimal("1500.00"),
                stock_quantity=5,
                specifications={
                    "size": "27 inch",
                    "resolution": "2560x1440",
                    "refresh_rate": "60Hz",
                },
                is_active=True,
            ),

            # -------------------------
            # Inactive variant
            # Useful for testing is_active
            # -------------------------

            ProductVariant(
                product_id=products[3].id,
                sku="HP-PAV-OLD",
                name="Old Configuration",
                price=Decimal("49999.00"),
                discount=Decimal("5000.00"),
                stock_quantity=20,
                specifications={
                    "ram": "8GB",
                    "storage": "256GB SSD",
                },
                is_active=False,
            ),
        ]

        session.add_all(variants)

        await session.commit()

        print("Database seeded successfully.")
        print(f"Categories : {len([laptops, phones, headphones, monitors])}")
        print(f"Products   : {len(products)}")
        print(f"Variants   : {len(variants)}")


if __name__ == "__main__":
    asyncio.run(seed_database())