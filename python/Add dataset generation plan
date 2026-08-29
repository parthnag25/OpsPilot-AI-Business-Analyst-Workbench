import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# OpsPilot AI: Synthetic Supply Chain Data Generator
# ---------------------------------------------------------
# This script creates synthetic supply chain datasets for:
# - date dimension
# - products
# - suppliers
# - warehouses
# - customers
# - orders
# - shipments
# - inventory
# - returns
#
# Output folder:
# data/raw/
# ---------------------------------------------------------


RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Save a dataframe to the raw data folder."""
    path = os.path.join(RAW_DATA_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Saved {filename}: {len(df):,} rows")


def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """Return a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


# ---------------------------------------------------------
# 1. Date dimension
# ---------------------------------------------------------

def create_dim_date() -> pd.DataFrame:
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    dim_date = pd.DataFrame({
        "date_key": dates.strftime("%Y%m%d").astype(int),
        "full_date": dates.date,
        "year": dates.year,
        "quarter": dates.quarter,
        "month": dates.month,
        "month_name": dates.strftime("%B"),
        "week_number": dates.isocalendar().week.astype(int),
        "day_name": dates.strftime("%A")
    })

    return dim_date


# ---------------------------------------------------------
# 2. Supplier dimension
# ---------------------------------------------------------

def create_dim_supplier() -> pd.DataFrame:
    regions = ["Northeast", "Midwest", "South", "West"]

    suppliers = []
    for i in range(1, 26):
        supplier_id = f"SUP{i:03d}"
        supplier_region = random.choice(regions)

        # Some suppliers are intentionally riskier
        risk_score = np.random.choice(
            range(1, 11),
            p=[0.08, 0.10, 0.12, 0.15, 0.15, 0.13, 0.10, 0.08, 0.06, 0.03]
        )

        standard_lead_time_days = int(np.random.randint(3, 15) + risk_score * 0.4)

        suppliers.append({
            "supplier_id": supplier_id,
            "supplier_name": f"Supplier {i}",
            "supplier_region": supplier_region,
            "standard_lead_time_days": standard_lead_time_days,
            "supplier_risk_score": int(risk_score)
        })

    return pd.DataFrame(suppliers)


# ---------------------------------------------------------
# 3. Product dimension
# ---------------------------------------------------------

def create_dim_product(dim_supplier: pd.DataFrame) -> pd.DataFrame:
    categories = {
        "Electronics": ["Mobile Accessories", "Computer Accessories", "Smart Devices"],
        "Home Goods": ["Kitchen", "Storage", "Furniture"],
        "Grocery": ["Packaged Food", "Beverages", "Snacks"],
        "Apparel": ["Men", "Women", "Footwear"],
        "Health & Personal Care": ["Personal Care", "Wellness", "Cleaning"],
        "Office Supplies": ["Paper", "Writing", "Desk Accessories"]
    }

    products = []
    supplier_ids = dim_supplier["supplier_id"].tolist()

    for i in range(1, 101):
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])
        supplier_id = random.choice(supplier_ids)

        unit_cost = round(np.random.uniform(5, 250), 2)
        markup = np.random.uniform(1.25, 2.20)
        unit_price = round(unit_cost * markup, 2)

        products.append({
            "product_id": f"PROD{i:03d}",
            "product_name": f"{subcategory} Product {i}",
            "category": category,
            "subcategory": subcategory,
            "unit_cost": unit_cost,
            "unit_price": unit_price,
            "supplier_id": supplier_id
        })

    return pd.DataFrame(products)


# ---------------------------------------------------------
# 4. Warehouse dimension
# ---------------------------------------------------------

def create_dim_warehouse() -> pd.DataFrame:
    warehouse_data = [
        ("WH001", "Chicago Fulfillment Center", "Midwest", "IL"),
        ("WH002", "Dallas Distribution Hub", "South", "TX"),
        ("WH003", "Atlanta Operations Center", "South", "GA"),
        ("WH004", "Los Angeles Fulfillment Center", "West", "CA"),
        ("WH005", "Seattle Distribution Hub", "West", "WA"),
        ("WH006", "New Jersey Fulfillment Center", "Northeast", "NJ"),
        ("WH007", "Boston Logistics Center", "Northeast", "MA"),
        ("WH008", "Denver Operations Center", "West", "CO"),
        ("WH009", "Columbus Distribution Hub", "Midwest", "OH"),
        ("WH010", "Phoenix Fulfillment Center", "West", "AZ")
    ]

    warehouses = []
    for warehouse_id, warehouse_name, region, state in warehouse_data:
        warehouses.append({
            "warehouse_id": warehouse_id,
            "warehouse_name": warehouse_name,
            "region": region,
            "state": state,
            "capacity_units": int(np.random.randint(50000, 150000)),
            "labor_hours_available": int(np.random.randint(8000, 25000))
        })

    return pd.DataFrame(warehouses)


# ---------------------------------------------------------
# 5. Customer dimension
# ---------------------------------------------------------

def create_dim_customer() -> pd.DataFrame:
    regions_states = {
        "Northeast": ["NY", "NJ", "MA", "PA", "CT"],
        "Midwest": ["IL", "OH", "MI", "WI", "IN"],
        "South": ["TX", "GA", "FL", "NC", "TN"],
        "West": ["CA", "WA", "AZ", "CO", "OR"]
    }

    segments = ["Retail", "Wholesale", "Enterprise"]

    customers = []
    for i in range(1, 2001):
        region = random.choice(list(regions_states.keys()))
        state = random.choice(regions_states[region])
        segment = np.random.choice(segments, p=[0.65, 0.25, 0.10])

        customers.append({
            "customer_id": f"CUST{i:05d}",
            "customer_segment": segment,
            "state": state,
            "region": region
        })

    return pd.DataFrame(customers)


# ---------------------------------------------------------
# 6. Orders fact table
# ---------------------------------------------------------

def create_fact_orders(
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_warehouse: pd.DataFrame
) -> pd.DataFrame:
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 20)

    customers = dim_customer["customer_id"].tolist()
    products = dim_product[["product_id", "unit_price"]].to_dict("records")
    warehouses = dim_warehouse["warehouse_id"].tolist()

    orders = []

    for i in range(1, 25001):
        order_id = f"ORD{i:06d}"
        order_date = random_date(start_date, end_date)
        promised_delivery_date = order_date + timedelta(days=random.randint(2, 7))

        product = random.choice(products)
        quantity_ordered = int(np.random.choice([1, 2, 3, 4, 5, 10, 15, 20],
                                                p=[0.25, 0.22, 0.16, 0.10, 0.08, 0.08, 0.06, 0.05]))

        order_value = round(quantity_ordered * product["unit_price"], 2)

        warehouse_id = random.choice(warehouses)

        # Warehouse-level delay pressure
        delay_probability = {
            "WH001": 0.13,
            "WH002": 0.15,
            "WH003": 0.12,
            "WH004": 0.18,
            "WH005": 0.16,
            "WH006": 0.10,
            "WH007": 0.09,
            "WH008": 0.14,
            "WH009": 0.17,
            "WH010": 0.13
        }[warehouse_id]

        is_cancelled = np.random.random() < 0.025
        is_delayed = np.random.random() < delay_probability

        if is_cancelled:
            order_status = "Cancelled"
            actual_delivery_date = None
        elif is_delayed:
            order_status = "Delayed"
            actual_delivery_date = promised_delivery_date + timedelta(days=random.randint(1, 8))
        else:
            order_status = "Delivered"
            actual_delivery_date = promised_delivery_date - timedelta(days=random.randint(0, 2))

        orders.append({
            "order_id": order_id,
            "order_date": order_date.date(),
            "customer_id": random.choice(customers),
            "product_id": product["product_id"],
            "warehouse_id": warehouse_id,
            "quantity_ordered": quantity_ordered,
            "order_value": order_value,
            "promised_delivery_date": promised_delivery_date.date(),
            "actual_delivery_date": actual_delivery_date.date() if actual_delivery_date else None,
            "order_status": order_status
        })

    return pd.DataFrame(orders)


# ---------------------------------------------------------
# 7. Shipments fact table
# ---------------------------------------------------------

def create_fact_shipments(fact_orders: pd.DataFrame) -> pd.DataFrame:
    carriers = ["FedEx", "UPS", "DHL", "USPS", "Regional Carrier"]
    shipping_methods = ["Standard", "Expedited", "Priority"]

    delay_reasons = [
        "Inventory Shortage",
        "Carrier Delay",
        "Labor Constraint",
        "Weather",
        "System Issue",
        "Supplier Delay"
    ]

    shipments = []

    delivered_orders = fact_orders[fact_orders["order_status"] != "Cancelled"].copy()

    for idx, row in delivered_orders.iterrows():
        shipment_id = f"SHP{idx + 1:06d}"

        if row["order_status"] == "Delayed":
            delay_days = (
                pd.to_datetime(row["actual_delivery_date"]) -
                pd.to_datetime(row["promised_delivery_date"])
            ).days
            delay_reason = random.choice(delay_reasons)
        else:
            delay_days = 0
            delay_reason = "No Delay"

        shipping_method = np.random.choice(shipping_methods, p=[0.65, 0.25, 0.10])

        base_cost = {
            "Standard": np.random.uniform(6, 18),
            "Expedited": np.random.uniform(15, 35),
            "Priority": np.random.uniform(25, 55)
        }[shipping_method]

        shipments.append({
            "shipment_id": shipment_id,
            "order_id": row["order_id"],
            "carrier": random.choice(carriers),
            "shipping_method": shipping_method,
            "shipping_cost": round(base_cost + delay_days * 1.75, 2),
            "delay_days": int(delay_days),
            "delay_reason": delay_reason
        })

    return pd.DataFrame(shipments)


# ---------------------------------------------------------
# 8. Inventory fact table
# ---------------------------------------------------------

def create_fact_inventory(
    dim_date: pd.DataFrame,
    dim_product: pd.DataFrame,
    dim_warehouse: pd.DataFrame
) -> pd.DataFrame:
    products = dim_product["product_id"].tolist()
    warehouses = dim_warehouse["warehouse_id"].tolist()

    sampled_dates = dim_date.sample(n=300, random_state=RANDOM_SEED)["date_key"].tolist()

    records = []
    inventory_id = 1

    for date_key in sampled_dates:
        for warehouse_id in warehouses:
            selected_products = random.sample(products, 10)

            for product_id in selected_products:
                opening_stock = int(np.random.randint(50, 1500))
                demand_units = int(np.random.randint(10, 500))
                closing_stock = max(opening_stock - demand_units, 0)
                reorder_point = int(np.random.randint(100, 400))
                stockout_flag = closing_stock < reorder_point

                records.append({
                    "inventory_id": f"INV{inventory_id:07d}",
                    "date_key": int(date_key),
                    "product_id": product_id,
                    "warehouse_id": warehouse_id,
                    "opening_stock": opening_stock,
                    "closing_stock": closing_stock,
                    "reorder_point": reorder_point,
                    "stockout_flag": bool(stockout_flag)
                })

                inventory_id += 1

    return pd.DataFrame(records)


# ---------------------------------------------------------
# 9. Returns fact table
# ---------------------------------------------------------

def create_fact_returns(
    fact_orders: pd.DataFrame,
    fact_shipments: pd.DataFrame
) -> pd.DataFrame:
    return_reasons = [
        "Damaged Item",
        "Late Delivery",
        "Wrong Item",
        "Quality Issue",
        "Customer Changed Mind"
    ]

    orders_with_shipments = fact_orders.merge(
        fact_shipments[["order_id", "delay_days"]],
        on="order_id",
        how="left"
    )

    return_records = []
    return_id = 1

    for _, row in orders_with_shipments.iterrows():
        if row["order_status"] == "Cancelled":
            continue

        base_return_probability = 0.08

        # Late deliveries have a higher chance of return
        if row["delay_days"] and row["delay_days"] > 0:
            base_return_probability += 0.07

        # Higher-value orders have slightly higher return risk
        if row["order_value"] > 1000:
            base_return_probability += 0.03

        if np.random.random() < base_return_probability:
            return_date = pd.to_datetime(row["actual_delivery_date"]) + timedelta(days=random.randint(1, 20))

            reason = np.random.choice(
                return_reasons,
                p=[0.22, 0.25 if row["delay_days"] > 0 else 0.10, 0.15, 0.18, 0.20]
            )

            return_records.append({
                "return_id": f"RET{return_id:06d}",
                "order_id": row["order_id"],
                "product_id": row["product_id"],
                "return_date": return_date.date(),
                "return_reason": reason,
                "return_cost": round(np.random.uniform(10, 150), 2)
            })

            return_id += 1

    return pd.DataFrame(return_records)


# ---------------------------------------------------------
# Main execution
# ---------------------------------------------------------

def main() -> None:
    print("Generating OpsPilot AI synthetic supply chain dataset...")

    dim_date = create_dim_date()
    dim_supplier = create_dim_supplier()
    dim_product = create_dim_product(dim_supplier)
    dim_warehouse = create_dim_warehouse()
    dim_customer = create_dim_customer()

    fact_orders = create_fact_orders(dim_customer, dim_product, dim_warehouse)
    fact_shipments = create_fact_shipments(fact_orders)
    fact_inventory = create_fact_inventory(dim_date, dim_product, dim_warehouse)
    fact_returns = create_fact_returns(fact_orders, fact_shipments)

    save_csv(dim_date, "dim_date.csv")
    save_csv(dim_supplier, "dim_supplier.csv")
    save_csv(dim_product, "dim_product.csv")
    save_csv(dim_warehouse, "dim_warehouse.csv")
    save_csv(dim_customer, "dim_customer.csv")
    save_csv(fact_orders, "fact_orders.csv")
    save_csv(fact_shipments, "fact_shipments.csv")
    save_csv(fact_inventory, "fact_inventory.csv")
    save_csv(fact_returns, "fact_returns.csv")

    print("Dataset generation complete.")


if __name__ == "__main__":
    main()
