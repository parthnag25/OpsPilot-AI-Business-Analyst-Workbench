# Dataset Generation Plan

## Project: OpsPilot AI

This document defines the planned synthetic dataset generation approach for OpsPilot AI. The dataset will simulate supply chain operations across customers, products, suppliers, warehouses, orders, shipments, inventory, and returns.

The goal is to create realistic business scenarios that support KPI analysis, AI-assisted business analysis, Jira-style requirement generation, and Power BI dashboard development.

---

## Dataset Scope

The synthetic dataset will include:

| Table | Planned Record Count |
|---|---:|
| dim_date | 730 records |
| dim_product | 100 records |
| dim_supplier | 25 records |
| dim_warehouse | 10 records |
| dim_customer | 2,000 records |
| fact_orders | 25,000 records |
| fact_shipments | 25,000 records |
| fact_inventory | 30,000 records |
| fact_returns | 2,000–4,000 records |

---

## Time Period

The dataset will cover:

```text
January 1, 2024 to December 31, 2025
