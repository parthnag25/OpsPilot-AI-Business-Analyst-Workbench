# Data Dictionary

## Project: OpsPilot AI

This data dictionary defines the planned synthetic supply chain dataset for OpsPilot AI. The dataset will support supply chain KPI analysis, AI-assisted business analysis, Jira-style requirement generation, and Power BI dashboard development.

The dataset is designed around common supply chain operations such as orders, shipments, inventory, suppliers, warehouses, customers, and returns.

---

## 1. dim_date

The date dimension supports time-based analysis across orders, shipments, inventory, and returns.

| Column Name | Description |
|---|---|
| date_key | Unique date identifier |
| full_date | Actual calendar date |
| year | Calendar year |
| quarter | Calendar quarter |
| month | Calendar month number |
| month_name | Calendar month name |
| week_number | Week number of the year |
| day_name | Day of the week |

---

## 2. dim_product

The product dimension contains product-level details used to analyze sales, inventory, stockout risk, and return patterns.

| Column Name | Description |
|---|---|
| product_id | Unique product identifier |
| product_name | Product name |
| category | Product category |
| subcategory | Product subcategory |
| unit_cost | Cost per unit |
| unit_price | Selling price per unit |
| supplier_id | Supplier linked to the product |

---

## 3. dim_supplier

The supplier dimension supports supplier performance, lead-time, and delay analysis.

| Column Name | Description |
|---|---|
| supplier_id | Unique supplier identifier |
| supplier_name | Supplier name |
| supplier_region | Supplier operating region |
| standard_lead_time_days | Expected supplier lead time |
| supplier_risk_score | Supplier risk rating from 1 to 10 |

---

## 4. dim_warehouse

The warehouse dimension supports analysis of warehouse utilization, late shipments, capacity, and fulfillment performance.

| Column Name | Description |
|---|---|
| warehouse_id | Unique warehouse identifier |
| warehouse_name | Warehouse name |
| region | Warehouse region |
| state | Warehouse state |
| capacity_units | Total warehouse unit capacity |
| labor_hours_available | Available labor hours |

---

## 5. dim_customer

The customer dimension supports regional and segment-level order analysis.

| Column Name | Description |
|---|---|
| customer_id | Unique customer identifier |
| customer_segment | Customer segment such as Retail, Wholesale, or Enterprise |
| state | Customer state |
| region | Customer region |

---

## 6. fact_orders

The orders fact table contains order-level transactions used to analyze revenue, fulfillment, order volume, and customer demand.

| Column Name | Description |
|---|---|
| order_id | Unique order identifier |
| order_date | Date when the order was placed |
| customer_id | Customer linked to the order |
| product_id | Product ordered |
| warehouse_id | Warehouse responsible for fulfillment |
| quantity_ordered | Number of units ordered |
| order_value | Total order value |
| promised_delivery_date | Expected delivery date |
| actual_delivery_date | Actual delivery date |
| order_status | Delivered, Delayed, Cancelled, or Returned |

---

## 7. fact_shipments

The shipments fact table supports delivery performance, carrier analysis, shipping cost, and delay reason analysis.

| Column Name | Description |
|---|---|
| shipment_id | Unique shipment identifier |
| order_id | Order linked to the shipment |
| carrier | Shipping carrier |
| shipping_method | Standard, Expedited, or Priority |
| shipping_cost | Cost of shipping |
| delay_days | Number of days delayed |
| delay_reason | Inventory, Carrier, Labor, Weather, System, or No Delay |

---

## 8. fact_inventory

The inventory fact table supports stockout risk, inventory turnover, reorder point, and warehouse inventory analysis.

| Column Name | Description |
|---|---|
| inventory_id | Unique inventory record identifier |
| date_key | Date linked to the inventory record |
| product_id | Product linked to the inventory record |
| warehouse_id | Warehouse linked to the inventory record |
| opening_stock | Starting inventory level |
| closing_stock | Ending inventory level |
| reorder_point | Minimum inventory level before reorder |
| stockout_flag | Indicates whether stockout occurred |

---

## 9. fact_returns

The returns fact table supports return rate, return cost, product quality, and customer experience analysis.

| Column Name | Description |
|---|---|
| return_id | Unique return identifier |
| order_id | Order linked to the return |
| product_id | Product returned |
| return_date | Date of return |
| return_reason | Damaged, Late Delivery, Wrong Item, Quality Issue, or Customer Changed Mind |
| return_cost | Cost associated with the return |

---

# Planned KPIs

The dataset will support the following supply chain KPIs:

| KPI | Description |
|---|---|
| Total Orders | Count of total orders |
| Total Revenue | Sum of order value |
| On-Time Delivery Rate | Percentage of orders delivered on or before promised date |
| Late Shipment Rate | Percentage of orders delivered after promised date |
| Average Delay Days | Average number of delay days |
| Stockout Rate | Percentage of inventory records with stockout |
| Return Rate | Percentage of orders returned |
| Order Fulfillment Rate | Percentage of orders successfully fulfilled |
| Warehouse Utilization | Warehouse usage compared with total capacity |
| Supplier Delay Rate | Percentage of supplier-linked orders with delays |
| Shipping Cost per Order | Average shipping cost per order |

---

# AI / LLM Use Case

The dataset will be used by OpsPilot AI to generate structured LLM outputs such as:

- Business issue summaries
- Likely root-cause explanations
- Business requirements
- Jira-style epics
- User stories
- Acceptance criteria
- Executive-ready recommendations
- Risk levels
- Human review flags

Example:

A high late shipment rate in one warehouse can be converted into a business requirement and Jira-style user story for improving delivery visibility.

---

# Responsible AI Notes

AI-generated outputs will be treated as draft analysis. Final recommendations will require human review before being considered approved business actions.
