# SQL KPI Results Summary

## Project: OpsPilot AI

This document summarizes the SQL KPI analysis results for the OpsPilot AI project. The analysis was performed using PostgreSQL on the validated synthetic supply chain dataset.

The purpose of this analysis is to identify operational risks across orders, shipments, inventory, warehouses, suppliers, product categories, and customer segments. These results will support Power BI dashboard development, AI-assisted business analysis, LLM-based requirement generation, and Jira-style user story creation.

---

## 1. Executive KPI Summary

| KPI | Result |
|---|---:|
| Total Orders | 25,000 |
| Total Revenue | $24,880,425.10 |
| Order Fulfillment Rate | 97.47% |
| On-Time Delivery Rate | 86.82% |
| Late Shipment Rate | 13.18% |
| Average Delay Days | 0.60 |
| Stockout Rate | 31.64% |
| Return Rate | 9.62% |
| Shipping Cost per Order | $19.08 |

### Business Insight

OpsPilot AI analyzed 25,000 supply chain orders and identified a 13.18% late shipment rate, 31.64% stockout rate, and 9.62% return rate. The strongest operational concern is stockout risk, followed by late shipments and return exposure.

---

## 2. Warehouse Performance Analysis

### Highest Late Shipment Risk Warehouses

| Rank | Warehouse | Region | Late Shipment Rate |
|---:|---|---|---:|
| 1 | Los Angeles Fulfillment Center | West | 17.13% |
| 2 | Columbus Distribution Hub | Midwest | 16.64% |
| 3 | Dallas Distribution Hub | South | 15.32% |
| 4 | Seattle Distribution Hub | West | 14.98% |
| 5 | Denver Operations Center | West | 13.53% |

### Business Insight

Los Angeles, Columbus, and Dallas are the highest-risk warehouses for late shipments. Since order volume is fairly similar across warehouses, the delay issue is likely not caused only by volume. It may indicate warehouse-level operational pressure, labor constraints, fulfillment bottlenecks, carrier issues, or inventory availability problems.

---

## 3. Product Category Stockout Risk

### Highest Stockout Risk Areas

| Rank | Category | Subcategory | Stockout Rate |
|---:|---|---|---:|
| 1 | Electronics | Computer Accessories | 34.81% |
| 2 | Health & Personal Care | Personal Care | 33.07% |
| 3 | Electronics | Smart Devices | 33.05% |
| 4 | Grocery | Packaged Food | 32.94% |
| 5 | Office Supplies | Writing | 31.99% |

### Business Insight

Electronics has two of the highest stockout-risk subcategories: Computer Accessories and Smart Devices. This suggests that demand planning, reorder points, or supplier replenishment timing may need review for high-demand electronics products.

---

## 4. Supplier Delay Risk Analysis

### Highest Supplier Delay Risk

| Rank | Supplier | Region | Supplier Delay Rate |
|---:|---|---|---:|
| 1 | Supplier 17 | West | 15.60% |
| 2 | Supplier 2 | Northeast | 15.02% |
| 3 | Supplier 9 | West | 14.75% |
| 4 | Supplier 20 | South | 14.31% |
| 5 | Supplier 14 | Midwest | 14.17% |

### Business Insight

Supplier 17 had the highest supplier delay rate at 15.60%, followed by Supplier 2 at 15.02% and Supplier 9 at 14.75%. These suppliers should be reviewed for lead-time reliability, fulfillment consistency, and backup supplier options.

Supplier risk score does not fully explain delay performance. For example, Supplier 9 has a low supplier risk score but still shows a high delay rate. This suggests delay risk may also be connected to product mix, warehouse fulfillment, demand pressure, or carrier performance.

---

## 5. Delay Reason Analysis

| Delay Reason | Shipment Count | Shipment Share | Average Delay Days | Total Shipping Cost |
|---|---:|---:|---:|---:|
| No Delay | 21,156 | 86.82% | 0.00 | $381,565.38 |
| Weather | 558 | 2.29% | 4.68 | $14,940.38 |
| Labor Constraint | 540 | 2.22% | 4.49 | $13,554.80 |
| Inventory Shortage | 540 | 2.22% | 4.44 | $14,032.26 |
| System Issue | 531 | 2.18% | 4.60 | $14,006.59 |
| Supplier Delay | 523 | 2.15% | 4.47 | $13,347.23 |
| Carrier Delay | 520 | 2.13% | 4.53 | $13,473.86 |

### Business Insight

No-delay shipments represent 86.82% of all shipments. Among delayed shipments, Weather was the largest delay reason with 558 shipments and an average delay of 4.68 days. Labor Constraint and Inventory Shortage followed closely with 540 shipments each.

The delay pattern suggests that late shipments are not caused by one single issue. They are a multi-driver operational problem involving weather, labor, inventory, systems, suppliers, and carriers.

---

## 6. Return Analysis by Product Category

| Category | Total Orders | Total Returns | Return Rate | Total Return Cost | Late Delivery Returns |
|---|---:|---:|---:|---:|---:|
| Apparel | 5,111 | 516 | 10.10% | $40,832.71 | 55 |
| Electronics | 3,774 | 371 | 9.83% | $29,586.47 | 45 |
| Office Supplies | 4,929 | 478 | 9.70% | $37,198.21 | 59 |
| Home Goods | 3,769 | 365 | 9.68% | $28,609.30 | 35 |
| Grocery | 4,254 | 401 | 9.43% | $31,947.23 | 54 |
| Health & Personal Care | 3,163 | 274 | 8.66% | $22,228.63 | 35 |

### Business Insight

Apparel had the highest return rate at 10.10% and the highest return cost at $40,832.71. This suggests Apparel should be prioritized for review around sizing, product quality, fulfillment accuracy, customer expectations, or delivery experience.

Office Supplies also has a high total return cost at $37,198.21, making it another category worth reviewing from a cost-control perspective.

---

## 7. Customer Segment Performance

### Revenue Priority

Retail customers generated the highest revenue across all regions.

| Segment | Region | Total Revenue |
|---|---|---:|
| Retail | Northeast | $4,246,620.26 |
| Retail | South | $4,223,677.06 |
| Retail | West | $4,125,687.13 |
| Retail | Midwest | $3,661,821.27 |

### Highest Late Shipment Risk

| Segment | Region | Late Shipment Rate |
|---|---|---:|
| Wholesale | West | 14.39% |
| Wholesale | Northeast | 14.06% |
| Enterprise | Midwest | 13.88% |
| Wholesale | South | 13.69% |
| Retail | Midwest | 13.41% |

### Highest Return Risk

| Segment | Region | Return Rate |
|---|---|---:|
| Enterprise | South | 11.64% |
| Wholesale | Northeast | 10.91% |
| Wholesale | Midwest | 10.81% |
| Retail | Midwest | 10.56% |
| Wholesale | West | 10.56% |

### Business Insight

Retail is the main revenue driver, especially in the Northeast, South, and West regions. However, operational risk is higher in Wholesale and Enterprise segments, where late shipment and return rates are more elevated.

This creates three different business priorities:

- Retail: revenue protection
- Wholesale: delivery performance improvement
- Enterprise: return reduction and customer experience review

---

## 8. AI Issue Candidate Table

The AI issue candidate query converts SQL KPI findings into structured operational issue records. These issue records will be used as inputs for the LLM workflow to generate business requirements, Jira-style user stories, acceptance criteria, risk levels, and executive recommendations.

### High Severity Issues

| Issue Type | Business Area | Metric | Value | Severity |
|---|---|---|---:|---|
| Product Stockout Risk | Grocery | Stockout Rate | 31.93% | High |
| Product Stockout Risk | Electronics | Stockout Rate | 31.76% | High |
| Product Stockout Risk | Health & Personal Care | Stockout Rate | 31.71% | High |
| Product Stockout Risk | Office Supplies | Stockout Rate | 31.69% | High |
| Product Stockout Risk | Apparel | Stockout Rate | 31.53% | High |
| Product Stockout Risk | Home Goods | Stockout Rate | 31.19% | High |

### Medium Severity Issues

| Issue Type | Business Area | Metric | Value | Severity |
|---|---|---|---:|---|
| Warehouse Delay Risk | Los Angeles Fulfillment Center | Late Shipment Rate | 17.13% | Medium |
| Warehouse Delay Risk | Columbus Distribution Hub | Late Shipment Rate | 16.64% | Medium |
| Supplier Delay Risk | Supplier 17 | Supplier Delay Rate | 15.60% | Medium |
| Warehouse Delay Risk | Dallas Distribution Hub | Late Shipment Rate | 15.32% | Medium |
| Supplier Delay Risk | Supplier 2 | Supplier Delay Rate | 15.02% | Medium |

### Business Insight

OpsPilot AI identified product stockout risk as the highest-priority operational issue, with all major product categories showing stockout rates above 31%. Grocery had the highest stockout rate at 31.93%, followed by Electronics at 31.76% and Health & Personal Care at 31.71%.

Warehouse and supplier delay risks were mostly medium severity, led by Los Angeles Fulfillment Center at 17.13% late shipment rate and Supplier 17 at 15.60% supplier delay rate.

---

## Overall Recommendation

The highest-priority recommendation is to review inventory planning and replenishment logic because stockout risk is above 31% across all major product categories.

Secondary recommendations include:

1. Review warehouse operations at Los Angeles, Columbus, and Dallas.
2. Review supplier reliability for Supplier 17, Supplier 2, and Supplier 9.
3. Investigate delay drivers across weather, labor constraints, inventory shortages, system issues, supplier delays, and carrier delays.
4. Prioritize Apparel for return-rate and return-cost reduction.
5. Protect Retail revenue while improving delivery performance for Wholesale and return performance for Enterprise.

---

## How This Supports the AI Workflow

These SQL results will be used by the OpsPilot AI workflow to generate:

- Business issue summaries
- Root-cause hypotheses
- Business requirements
- Jira epics
- Jira-style user stories
- Acceptance criteria
- Executive-ready recommendations
- Risk levels
- Human review flags
