# PostgreSQL Load Validation

## Project: OpsPilot AI

This document confirms that the synthetic supply chain datasets were loaded into the PostgreSQL database for OpsPilot AI.

---

## Database Details

| Item | Value |
|---|---|
| Database Name | opspilot_ai |
| Schema Name | opspilot |
| Database Tool | PostgreSQL / pgAdmin |
| Data Source | Synthetic CSV files from data/raw |
| Load Method | pgAdmin Import/Export Data |

---

## Load Order

The CSV files were loaded in the following order to maintain primary key and foreign key relationships:

1. dim_date
2. dim_supplier
3. dim_warehouse
4. dim_customer
5. dim_product
6. fact_orders
7. fact_shipments
8. fact_inventory
9. fact_returns

---

## Row Count Validation

The following query was used to validate that all tables were loaded successfully:

```sql
SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count FROM opspilot.dim_customer
UNION ALL
SELECT 'dim_date', COUNT(*) FROM opspilot.dim_date
UNION ALL
SELECT 'dim_product', COUNT(*) FROM opspilot.dim_product
UNION ALL
SELECT 'dim_supplier', COUNT(*) FROM opspilot.dim_supplier
UNION ALL
SELECT 'dim_warehouse', COUNT(*) FROM opspilot.dim_warehouse
UNION ALL
SELECT 'fact_inventory', COUNT(*) FROM opspilot.fact_inventory
UNION ALL
SELECT 'fact_orders', COUNT(*) FROM opspilot.fact_orders
UNION ALL
SELECT 'fact_returns', COUNT(*) FROM opspilot.fact_returns
UNION ALL
SELECT 'fact_shipments', COUNT(*) FROM opspilot.fact_shipments
ORDER BY table_name;
