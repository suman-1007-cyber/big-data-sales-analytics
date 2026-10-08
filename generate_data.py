from pathlib import Path

import numpy as np
import pandas as pd


PRODUCTS = [
    ("Laptop Pro 14", "Electronics", 850),
    ("Laptop Air 13", "Electronics", 720),
    ("Smartphone X", "Electronics", 540),
    ("Smartphone Lite", "Electronics", 280),
    ("Tablet Plus", "Electronics", 360),

    ("Wireless Headphones", "Accessories", 95),
    ("Bluetooth Speaker", "Accessories", 70),
    ("Smart Watch", "Accessories", 145),
    ("Mechanical Keyboard", "Accessories", 85),
    ("Wireless Mouse", "Accessories", 35),

    ("4K Monitor", "Electronics", 310),
    ("USB-C Hub", "Accessories", 45),

    ("External SSD 1TB", "Storage", 110),
    ("External HDD 2TB", "Storage", 85),
    ("Memory Card 256GB", "Storage", 32),

    ("Office Chair", "Furniture", 190),
    ("Standing Desk", "Furniture", 320),
    ("Desk Lamp", "Furniture", 42),
    ("Bookshelf", "Furniture", 135),
    ("Filing Cabinet", "Furniture", 160),

    ("Printer", "Office", 210),
    ("Laser Printer", "Office", 390),
    ("Paper Pack", "Office", 8),
    ("Ink Cartridge", "Office", 28),
    ("Projector", "Office", 520),

    ("Backpack", "Lifestyle", 55),
    ("Travel Bag", "Lifestyle", 78),
    ("Water Bottle", "Lifestyle", 18),
    ("Fitness Band", "Lifestyle", 48),
    ("Desk Organizer", "Lifestyle", 22),
]


REGIONS = [
    "North",
    "South",
    "East",
    "West",
    "Central",
]


def generate_dataset(
    n_records=50000,
    seed=42,
    output_path="data/sales_data.csv",
):

    rng = np.random.default_rng(seed)

    product_names = np.array(
        [product[0] for product in PRODUCTS]
    )

    categories = np.array(
        [product[1] for product in PRODUCTS]
    )

    base_prices = np.array(
        [product[2] for product in PRODUCTS],
        dtype=float,
    )

    # Random product selection
    product_index = rng.integers(
        0,
        len(PRODUCTS),
        size=n_records,
    )

    # Random dates
    dates = (
        pd.Timestamp("2025-01-01")
        + pd.to_timedelta(
            rng.integers(
                0,
                639,
                size=n_records,
            ),
            unit="D",
        )
    )

    # Quantity
    quantities = rng.integers(
        1,
        11,
        size=n_records,
    )

    # Price variation
    unit_prices = np.round(
        base_prices[product_index]
        * rng.uniform(
            0.85,
            1.15,
            size=n_records,
        ),
        2,
    )

    # Discount between 0% and 30%
    discounts = np.round(
        rng.uniform(
            0.00,
            0.30,
            size=n_records,
        ),
        2,
    )

    df = pd.DataFrame(
        {
            "order_id": [
                f"ORD-{i:06d}"
                for i in range(
                    1,
                    n_records + 1,
                )
            ],

            "order_date": dates,

            "product_id": [
                f"P-{i + 1:03d}"
                for i in product_index
            ],

            "product_name":
                product_names[product_index],

            "category":
                categories[product_index],

            "region":
                rng.choice(
                    REGIONS,
                    size=n_records,
                ),

            "customer_id": [
                f"CUST-{i:04d}"
                for i in rng.integers(
                    1,
                    2001,
                    size=n_records,
                )
            ],

            "quantity": quantities,

            "unit_price": unit_prices,

            "discount": discounts,
        }
    )

    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output,
        index=False,
    )

    return df


if __name__ == "__main__":

    df = generate_dataset()

    print(
        f"Generated {len(df):,} sales records."
    )

    print(
        "Saved to data/sales_data.csv"
    )