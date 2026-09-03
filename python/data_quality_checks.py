import os
import pandas as pd


# ---------------------------------------------------------
# OpsPilot AI: Data Quality Checks
# ---------------------------------------------------------
# This script validates the generated synthetic supply chain
# datasets before they are used for SQL analysis, Power BI,
# and AI-assisted business analysis.
# ---------------------------------------------------------


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
REPORT_DIR = os.path.join(BASE_DIR, "docs")
REPORT_PATH = os.path.join(REPORT_DIR, "data_quality_report.md")


def load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV file from the raw data folder."""
    path = os.path.join(RAW_DATA_DIR, filename)
    return pd.read_csv(path)


def check_duplicate_ids(df: pd.DataFrame, id_column: str, table_name: str, results: list) -> None:
    duplicate_count = df[id_column].duplicated().sum()

    if duplicate_count == 0:
        results.append(f"- PASS: `{table_name}` has no duplicate `{id_column}` values.")
    else:
        results.append(f"- FAIL: `{table_name}` has {duplicate_count} duplicate `{id_column}` values.")


def check_missing_values(df: pd.DataFrame, table_name: str, results: list) -> None:
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if missing_values.empty:
        results.append(f"- PASS: `{table_name}` has no missing values.")
    else:
        results.append(f"- REVIEW: `{table_name}` has missing values:")
        for column, count in missing_values.items():
            results.append(f"  - `{column}`: {count} missing values")


def check_foreign_keys(
    fact_df: pd.DataFrame,
    dim_df: pd.DataFrame,
    fact_key: str,
    dim_key: str,
    fact_table: str,
    dim_table: str,
    results: list
) -> None:
    invalid_count = (~fact_df[fact_key].isin(dim_df[dim_key])).sum()

    if invalid_count == 0:
        results.append(f"- PASS: `{fact_table}.{fact_key}` values all exist in `{dim_table}.{dim_key}`.")
    else:
        results.append(f"- FAIL: `{fact_table}` has {invalid_count} invalid `{fact_key}` values not found in `{dim_table}`.")


def main() -> None:
    print("Running OpsPilot AI data quality checks...")

    results = []

    # Load datasets
    dim_date = load_csv("dim_date.csv")
    dim_supplier = load_csv("dim_supplier.csv")
    dim_product = load_csv("dim_product.csv")
    dim_warehouse = load_csv("dim_warehouse.csv")
    dim_customer = load_csv("dim_customer.csv")
    fact_orders = load_csv("fact_orders.csv")
    fact_shipments = load_csv("fact_shipments.csv")
    fact_inventory = load_csv("fact_inventory.csv")
    fact_returns = load_csv("fact_returns.csv")

    tables = {
        "dim_date": dim_date,
        "dim_supplier": dim_supplier,
        "dim_product": dim_product,
        "dim_warehouse": dim_warehouse,
        "dim_customer": dim_customer,
        "fact_orders": fact_orders,
        "fact_shipments": fact_shipments,
        "fact_inventory": fact_inventory,
        "fact_returns": fact_returns,
    }

    results.append("# Data Quality Report")
    results.append("")
    results.append("## Project: OpsPilot AI")
    results.append("")
    results.append("This report summarizes data quality checks performed on the synthetic supply chain dataset.")
    results.append("")

    # Row counts
    results.append("## 1. Row Counts")
    results.append("")
    for table_name, df in tables.items():
        results.append(f"- `{table_name}`: {len(df):,} rows")
    results.append("")

    # Missing values
    results.append("## 2. Missing Value Checks")
    results.append("")
    for table_name, df in tables.items():
        check_missing_values(df, table_name, results)
    results.append("")

    # Duplicate ID checks
    results.append("## 3. Duplicate Primary Key Checks")
    results.append("")
    check_duplicate_ids(dim_date, "date_key", "dim_date", results)
    check_duplicate_ids(dim_supplier, "supplier_id", "dim_supplier", results)
    check_duplicate_ids(dim_product, "product_id", "dim_product", results)
    check_duplicate_ids(dim_warehouse, "warehouse_id", "dim_warehouse", results)
    check_duplicate_ids(dim_customer, "customer_id", "dim_customer", results)
    check_duplicate_ids(fact_orders, "order_id", "fact_orders", results)
    check_duplicate_ids(fact_shipments, "shipment_id", "fact_shipments", results)
    check_duplicate_ids(fact_inventory, "inventory_id", "fact_inventory", results)
    check_duplicate_ids(fact_returns, "return_id", "fact_returns", results)
    results.append("")

    # Foreign key checks
    results.append("## 4. Foreign Key Checks")
    results.append("")
    check_foreign_keys(fact_orders, dim_customer, "customer_id", "customer_id", "fact_orders", "dim_customer", results)
    check_foreign_keys(fact_orders, dim_product, "product_id", "product_id", "fact_orders", "dim_product", results)
    check_foreign_keys(fact_orders, dim_warehouse, "warehouse_id", "warehouse_id", "fact_orders", "dim_warehouse", results)

    check_foreign_keys(fact_shipments, fact_orders, "order_id", "order_id", "fact_shipments", "fact_orders", results)

    check_foreign_keys(fact_inventory, dim_date, "date_key", "date_key", "fact_inventory", "dim_date", results)
    check_foreign_keys(fact_inventory, dim_product, "product_id", "product_id", "fact_inventory", "dim_product", results)
    check_foreign_keys(fact_inventory, dim_warehouse, "warehouse_id", "warehouse_id", "fact_inventory", "dim_warehouse", results)

    check_foreign_keys(fact_returns, fact_orders, "order_id", "order_id", "fact_returns", "fact_orders", results)
    check_foreign_keys(fact_returns, dim_product, "product_id", "product_id", "fact_returns", "dim_product", results)
    results.append("")

    # Business logic checks
    results.append("## 5. Business Logic Checks")
    results.append("")

    # Order values should not be negative
    negative_order_values = (fact_orders["order_value"] < 0).sum()
    if negative_order_values == 0:
        results.append("- PASS: No negative order values found.")
    else:
        results.append(f"- FAIL: {negative_order_values} negative order values found.")

    # Quantity ordered should be positive
    invalid_quantities = (fact_orders["quantity_ordered"] <= 0).sum()
    if invalid_quantities == 0:
        results.append("- PASS: All order quantities are positive.")
    else:
        results.append(f"- FAIL: {invalid_quantities} orders have invalid quantity values.")

    # Return costs should be positive
    invalid_return_costs = (fact_returns["return_cost"] <= 0).sum()
    if invalid_return_costs == 0:
        results.append("- PASS: All return costs are positive.")
    else:
        results.append(f"- FAIL: {invalid_return_costs} return records have invalid return costs.")

    # Delayed shipments should have delay_days > 0
    invalid_delays = fact_shipments[
        (fact_shipments["delay_reason"] != "No Delay") &
        (fact_shipments["delay_days"] <= 0)
    ]

    if len(invalid_delays) == 0:
        results.append("- PASS: Delayed shipment records have positive delay days.")
    else:
        results.append(f"- FAIL: {len(invalid_delays)} delayed shipment records have invalid delay days.")

    # No-delay shipments should have delay_days = 0
    invalid_no_delay = fact_shipments[
        (fact_shipments["delay_reason"] == "No Delay") &
        (fact_shipments["delay_days"] != 0)
    ]

    if len(invalid_no_delay) == 0:
        results.append("- PASS: No-delay shipment records have zero delay days.")
    else:
        results.append(f"- FAIL: {len(invalid_no_delay)} no-delay shipment records have invalid delay days.")

    # Stockout flag should be true when closing stock is below reorder point
    stockout_logic_issues = fact_inventory[
        (fact_inventory["closing_stock"] < fact_inventory["reorder_point"]) &
        (fact_inventory["stockout_flag"] != True)
    ]

    if len(stockout_logic_issues) == 0:
        results.append("- PASS: Stockout flag logic is consistent with closing stock and reorder point.")
    else:
        results.append(f"- FAIL: {len(stockout_logic_issues)} inventory records have stockout logic issues.")

    results.append("")

    # Summary
    results.append("## 6. Summary")
    results.append("")
    results.append("The synthetic supply chain dataset is ready for SQL analysis, Power BI dashboarding, and AI-assisted business analysis if all critical checks pass.")
    results.append("")
    results.append("AI-generated recommendations in later project stages will use this validated dataset as the supporting analytical foundation.")

    # Save report
    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write("\n".join(results))

    print(f"Data quality report created: {REPORT_PATH}")
    print("Data quality checks complete.")


if __name__ == "__main__":
    main()