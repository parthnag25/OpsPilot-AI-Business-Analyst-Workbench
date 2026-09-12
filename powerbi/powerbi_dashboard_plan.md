# Power BI Dashboard Plan

## Project: OpsPilot AI

This document defines the Power BI dashboard structure for the OpsPilot AI project.

The dashboard will visualize supply chain performance, operational risk, inventory stockout risk, warehouse delays, supplier delay risk, customer segment performance, and AI-generated business issue candidates.

---

## Dashboard Objective

The goal of the Power BI dashboard is to help business stakeholders identify operational risks and prioritize improvement actions.

The dashboard connects SQL-based KPI analysis with AI-assisted Business Analyst outputs.

The dashboard should answer the following business questions:

1. What is the overall supply chain performance?
2. Which product categories have the highest stockout risk?
3. Which warehouses have the highest late shipment rates?
4. Which suppliers are linked to delivery delay risk?
5. Which customer segments generate the most revenue and operational risk?
6. Which issues should be prioritized for business review?

---

## Data Sources

The dashboard will use PostgreSQL tables and views from the `opspilot_ai` database.

### PostgreSQL Views

| View | Purpose |
|---|---|
| opspilot.vw_executive_kpi_summary | Executive KPI cards |
| opspilot.vw_warehouse_performance | Warehouse delay and shipment performance |
| opspilot.vw_product_stockout_risk | Product category and subcategory stockout risk |
| opspilot.vw_supplier_delay_risk | Supplier delay risk analysis |
| opspilot.vw_ai_issue_candidates | AI-ready issue prioritization |

### CSV Outputs

| File | Purpose |
|---|---|
| data/processed/ai_business_outputs.csv | AI-assisted business summaries, requirements, and recommendations |
| jira/jira_user_stories.csv | Jira-style backlog and user stories |

---

## Dashboard Pages

## Page 1: Executive Overview

### Purpose

Provide a high-level view of total supply chain performance and risk.

### Visuals

| Visual | Fields |
|---|---|
| KPI Card | Total Orders |
| KPI Card | Total Revenue |
| KPI Card | Order Fulfillment Rate |
| KPI Card | On-Time Delivery Rate |
| KPI Card | Late Shipment Rate |
| KPI Card | Stockout Rate |
| KPI Card | Return Rate |
| KPI Card | Shipping Cost per Order |
| Bar Chart | Issue count by severity |
| Table | Top AI issue candidates |

### Main Insight

Stockout risk is the highest-priority operational issue, with stockout rates above 31% across all major product categories.

---

## Page 2: Inventory and Product Stockout Risk

### Purpose

Identify product categories and subcategories with the highest inventory risk.

### Visuals

| Visual | Fields |
|---|---|
| Bar Chart | Stockout Rate by Category |
| Bar Chart | Stockout Rate by Subcategory |
| Table | Category, Subcategory, Stockout Rate, Closing Stock, Reorder Point |
| KPI Card | Highest Stockout Rate |
| KPI Card | Average Stockout Rate |

### Main Insight

Grocery, Electronics, Health & Personal Care, Office Supplies, Apparel, and Home Goods all show high stockout risk above 31%.

---

## Page 3: Warehouse and Shipment Performance

### Purpose

Analyze fulfillment performance and identify warehouses with elevated late shipment risk.

### Visuals

| Visual | Fields |
|---|---|
| Bar Chart | Late Shipment Rate by Warehouse |
| Map or Bar Chart | Late Shipment Rate by Region |
| Table | Warehouse, Region, Total Orders, Late Shipments, Late Shipment Rate |
| KPI Card | Highest Warehouse Late Shipment Rate |
| KPI Card | Average Delay Days |

### Main Insight

Los Angeles Fulfillment Center, Columbus Distribution Hub, and Dallas Distribution Hub are the highest-risk warehouse locations for late shipments.

---

## Page 4: Supplier, Customer, and AI Recommendations

### Purpose

Connect supplier delay risk and customer segment performance with AI-generated business recommendations.

### Visuals

| Visual | Fields |
|---|---|
| Bar Chart | Supplier Delay Rate by Supplier |
| Table | Supplier, Supplier Region, Delay Rate, Risk Score |
| Bar Chart | Revenue by Customer Segment and Region |
| Table | Jira User Stories by Priority |
| Table | AI Business Issue Summary and Executive Recommendation |

### Main Insight

Supplier 17, Supplier 2, and Supplier 9 have the highest supplier delay rates. Retail drives the most revenue, while Wholesale and Enterprise show higher operational risk in delivery and returns.

---

## Recommended Slicers

Use the following slicers across dashboard pages where relevant:

| Slicer | Source |
|---|---|
| Severity | vw_ai_issue_candidates |
| Issue Type | vw_ai_issue_candidates |
| Region | warehouse/customer data |
| Category | product stockout risk |
| Supplier Region | supplier delay risk |
| Customer Segment | customer segment analysis |

---

## Design Rules

The dashboard should be clean, business-focused, and recruiter-friendly.

Recommended design principles:

1. Use a simple dark or light professional theme.
2. Keep KPI cards at the top of each page.
3. Use clear page titles.
4. Avoid overcrowding visuals.
5. Add short business insight text boxes on each page.
6. Prioritize business interpretation over excessive charts.
7. Use consistent formatting for percentages, currency, and counts.

---

## Business Analyst Value

This dashboard demonstrates the ability to:

- Connect PostgreSQL data to Power BI
- Build executive KPI reporting
- Analyze operational risks
- Identify stockout, delay, supplier, and customer issues
- Translate SQL outputs into business insights
- Support AI-assisted business requirement and Jira story generation
- Communicate findings to stakeholders

---

## Final Dashboard Deliverable

The final Power BI file will be saved as:

```text
powerbi/OpsPilot_AI_Dashboard.pbix
