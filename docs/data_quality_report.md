# Data Quality Report

## Project: OpsPilot AI

This report summarizes data quality checks performed on the synthetic supply chain dataset.

## 1. Row Counts

- `dim_date`: 731 rows
- `dim_supplier`: 25 rows
- `dim_product`: 100 rows
- `dim_warehouse`: 10 rows
- `dim_customer`: 2,000 rows
- `fact_orders`: 25,000 rows
- `fact_shipments`: 24,368 rows
- `fact_inventory`: 30,000 rows
- `fact_returns`: 2,405 rows

## 2. Missing Value Checks

- PASS: `dim_date` has no missing values.
- PASS: `dim_supplier` has no missing values.
- PASS: `dim_product` has no missing values.
- PASS: `dim_warehouse` has no missing values.
- PASS: `dim_customer` has no missing values.
- REVIEW: `fact_orders` has missing values:
  - `actual_delivery_date`: 632 missing values
- PASS: `fact_shipments` has no missing values.
- PASS: `fact_inventory` has no missing values.
- PASS: `fact_returns` has no missing values.

## 3. Duplicate Primary Key Checks

- PASS: `dim_date` has no duplicate `date_key` values.
- PASS: `dim_supplier` has no duplicate `supplier_id` values.
- PASS: `dim_product` has no duplicate `product_id` values.
- PASS: `dim_warehouse` has no duplicate `warehouse_id` values.
- PASS: `dim_customer` has no duplicate `customer_id` values.
- PASS: `fact_orders` has no duplicate `order_id` values.
- PASS: `fact_shipments` has no duplicate `shipment_id` values.
- PASS: `fact_inventory` has no duplicate `inventory_id` values.
- PASS: `fact_returns` has no duplicate `return_id` values.

## 4. Foreign Key Checks

- PASS: `fact_orders.customer_id` values all exist in `dim_customer.customer_id`.
- PASS: `fact_orders.product_id` values all exist in `dim_product.product_id`.
- PASS: `fact_orders.warehouse_id` values all exist in `dim_warehouse.warehouse_id`.
- PASS: `fact_shipments.order_id` values all exist in `fact_orders.order_id`.
- PASS: `fact_inventory.date_key` values all exist in `dim_date.date_key`.
- PASS: `fact_inventory.product_id` values all exist in `dim_product.product_id`.
- PASS: `fact_inventory.warehouse_id` values all exist in `dim_warehouse.warehouse_id`.
- PASS: `fact_returns.order_id` values all exist in `fact_orders.order_id`.
- PASS: `fact_returns.product_id` values all exist in `dim_product.product_id`.

## 5. Business Logic Checks

- PASS: No negative order values found.
- PASS: All order quantities are positive.
- PASS: All return costs are positive.
- PASS: Delayed shipment records have positive delay days.
- PASS: No-delay shipment records have zero delay days.
- PASS: Stockout flag logic is consistent with closing stock and reorder point.

## 6. Summary

The synthetic supply chain dataset is ready for SQL analysis, Power BI dashboarding, and AI-assisted business analysis if all critical checks pass.

AI-generated recommendations in later project stages will use this validated dataset as the supporting analytical foundation.