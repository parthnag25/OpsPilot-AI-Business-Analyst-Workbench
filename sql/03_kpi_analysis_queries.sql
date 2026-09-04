-- =========================================================
-- OpsPilot AI: SQL KPI Analysis Queries
-- Project: Agentic Business Analyst Workbench
-- Purpose: Analyze supply chain KPIs for business insights,
--          dashboard development, and AI-assisted recommendations
-- =========================================================


-- =========================================================
-- 1. Executive KPI Summary
-- =========================================================

SELECT
    (SELECT COUNT(*) FROM opspilot.fact_orders) AS total_orders,

    (SELECT ROUND(SUM(order_value), 2)
     FROM opspilot.fact_orders
     WHERE order_status <> 'Cancelled') AS total_revenue,

    (SELECT ROUND(
        100.0 * SUM(CASE WHEN order_status <> 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*),
        2
     )
     FROM opspilot.fact_orders) AS order_fulfillment_rate_pct,

    (SELECT ROUND(
        100.0 * SUM(CASE WHEN delay_days = 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
     )
     FROM opspilot.fact_shipments) AS on_time_delivery_rate_pct,

    (SELECT ROUND(
        100.0 * SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END) / COUNT(*),
        2
     )
     FROM opspilot.fact_shipments) AS late_shipment_rate_pct,

    (SELECT ROUND(AVG(delay_days), 2)
     FROM opspilot.fact_shipments) AS average_delay_days,

    (SELECT ROUND(
        100.0 * SUM(CASE WHEN stockout_flag = TRUE THEN 1 ELSE 0 END) / COUNT(*),
        2
     )
     FROM opspilot.fact_inventory) AS stockout_rate_pct,

    (SELECT ROUND(
        100.0 * COUNT(DISTINCT order_id) / (SELECT COUNT(*) FROM opspilot.fact_orders),
        2
     )
     FROM opspilot.fact_returns) AS return_rate_pct,

    (SELECT ROUND(AVG(shipping_cost), 2)
     FROM opspilot.fact_shipments) AS shipping_cost_per_order;


-- =========================================================
-- 2. Warehouse Performance Analysis
-- =========================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    w.region,
    w.state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_revenue,
    SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) AS late_shipments,
    ROUND(
        100.0 * SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(s.shipment_id),
        2
    ) AS late_shipment_rate_pct,
    ROUND(AVG(s.delay_days), 2) AS average_delay_days,
    ROUND(AVG(s.shipping_cost), 2) AS average_shipping_cost,
    w.capacity_units,
    w.labor_hours_available
FROM opspilot.fact_orders o
JOIN opspilot.dim_warehouse w
    ON o.warehouse_id = w.warehouse_id
JOIN opspilot.fact_shipments s
    ON o.order_id = s.order_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name,
    w.region,
    w.state,
    w.capacity_units,
    w.labor_hours_available
ORDER BY late_shipment_rate_pct DESC;


-- =========================================================
-- 3. Product Category Stockout Risk
-- =========================================================

SELECT
    p.category,
    p.subcategory,
    COUNT(i.inventory_id) AS inventory_records,
    SUM(CASE WHEN i.stockout_flag = TRUE THEN 1 ELSE 0 END) AS stockout_records,
    ROUND(
        100.0 * SUM(CASE WHEN i.stockout_flag = TRUE THEN 1 ELSE 0 END) / COUNT(i.inventory_id),
        2
    ) AS stockout_rate_pct,
    ROUND(AVG(i.opening_stock), 2) AS avg_opening_stock,
    ROUND(AVG(i.closing_stock), 2) AS avg_closing_stock,
    ROUND(AVG(i.reorder_point), 2) AS avg_reorder_point
FROM opspilot.fact_inventory i
JOIN opspilot.dim_product p
    ON i.product_id = p.product_id
GROUP BY
    p.category,
    p.subcategory
ORDER BY stockout_rate_pct DESC;


-- =========================================================
-- 4. Supplier Delay Risk Analysis
-- =========================================================

SELECT
    sup.supplier_id,
    sup.supplier_name,
    sup.supplier_region,
    sup.standard_lead_time_days,
    sup.supplier_risk_score,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        100.0 * SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(s.shipment_id),
        2
    ) AS supplier_delay_rate_pct,
    ROUND(AVG(s.delay_days), 2) AS avg_delay_days,
    ROUND(SUM(s.shipping_cost), 2) AS total_shipping_cost
FROM opspilot.dim_supplier sup
JOIN opspilot.dim_product p
    ON sup.supplier_id = p.supplier_id
JOIN opspilot.fact_orders o
    ON p.product_id = o.product_id
JOIN opspilot.fact_shipments s
    ON o.order_id = s.order_id
GROUP BY
    sup.supplier_id,
    sup.supplier_name,
    sup.supplier_region,
    sup.standard_lead_time_days,
    sup.supplier_risk_score
ORDER BY supplier_delay_rate_pct DESC;


-- =========================================================
-- 5. Delay Reason Analysis
-- =========================================================

SELECT
    delay_reason,
    COUNT(*) AS shipment_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM opspilot.fact_shipments),
        2
    ) AS shipment_share_pct,
    ROUND(AVG(delay_days), 2) AS average_delay_days,
    ROUND(SUM(shipping_cost), 2) AS total_shipping_cost
FROM opspilot.fact_shipments
GROUP BY delay_reason
ORDER BY shipment_count DESC;


-- =========================================================
-- 6. Return Analysis by Product Category
-- =========================================================

WITH orders_by_category AS (
    SELECT
        p.category,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM opspilot.fact_orders o
    JOIN opspilot.dim_product p
        ON o.product_id = p.product_id
    GROUP BY p.category
),

returns_by_category AS (
    SELECT
        p.category,
        COUNT(DISTINCT r.return_id) AS total_returns,
        ROUND(SUM(r.return_cost), 2) AS total_return_cost,
        SUM(CASE WHEN r.return_reason = 'Late Delivery' THEN 1 ELSE 0 END) AS late_delivery_returns
    FROM opspilot.fact_returns r
    JOIN opspilot.dim_product p
        ON r.product_id = p.product_id
    GROUP BY p.category
)

SELECT
    o.category,
    o.total_orders,
    COALESCE(r.total_returns, 0) AS total_returns,
    ROUND(
        100.0 * COALESCE(r.total_returns, 0) / o.total_orders,
        2
    ) AS return_rate_pct,
    COALESCE(r.total_return_cost, 0) AS total_return_cost,
    COALESCE(r.late_delivery_returns, 0) AS late_delivery_returns
FROM orders_by_category o
LEFT JOIN returns_by_category r
    ON o.category = r.category
ORDER BY return_rate_pct DESC;


-- =========================================================
-- 7. Customer Segment Performance
-- =========================================================

SELECT
    c.customer_segment,
    c.region,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_revenue,
    ROUND(AVG(o.order_value), 2) AS average_order_value,
    SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        100.0 * SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(s.shipment_id),
        2
    ) AS late_shipment_rate_pct,
    COUNT(DISTINCT r.return_id) AS total_returns,
    ROUND(
        100.0 * COUNT(DISTINCT r.return_id) / COUNT(DISTINCT o.order_id),
        2
    ) AS return_rate_pct
FROM opspilot.fact_orders o
JOIN opspilot.dim_customer c
    ON o.customer_id = c.customer_id
JOIN opspilot.fact_shipments s
    ON o.order_id = s.order_id
LEFT JOIN opspilot.fact_returns r
    ON o.order_id = r.order_id
GROUP BY
    c.customer_segment,
    c.region
ORDER BY total_revenue DESC;


-- =========================================================
-- 8. AI Issue Candidate Table
-- Purpose: Create structured KPI issues that can later be
--          passed into the LLM workflow for requirement
--          generation, Jira stories, and recommendations.
-- =========================================================

WITH warehouse_delay AS (
    SELECT
        'Warehouse Delay Risk' AS issue_type,
        w.warehouse_name AS business_area,
        ROUND(
            100.0 * SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(s.shipment_id),
            2
        ) AS metric_value,
        'Late Shipment Rate %' AS metric_name
    FROM opspilot.fact_orders o
    JOIN opspilot.dim_warehouse w
        ON o.warehouse_id = w.warehouse_id
    JOIN opspilot.fact_shipments s
        ON o.order_id = s.order_id
    GROUP BY w.warehouse_name
),

supplier_delay AS (
    SELECT
        'Supplier Delay Risk' AS issue_type,
        sup.supplier_name AS business_area,
        ROUND(
            100.0 * SUM(CASE WHEN s.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(s.shipment_id),
            2
        ) AS metric_value,
        'Supplier Delay Rate %' AS metric_name
    FROM opspilot.dim_supplier sup
    JOIN opspilot.dim_product p
        ON sup.supplier_id = p.supplier_id
    JOIN opspilot.fact_orders o
        ON p.product_id = o.product_id
    JOIN opspilot.fact_shipments s
        ON o.order_id = s.order_id
    GROUP BY sup.supplier_name
),

stockout_risk AS (
    SELECT
        'Product Stockout Risk' AS issue_type,
        p.category AS business_area,
        ROUND(
            100.0 * SUM(CASE WHEN i.stockout_flag = TRUE THEN 1 ELSE 0 END) / COUNT(i.inventory_id),
            2
        ) AS metric_value,
        'Stockout Rate %' AS metric_name
    FROM opspilot.fact_inventory i
    JOIN opspilot.dim_product p
        ON i.product_id = p.product_id
    GROUP BY p.category
)

SELECT
    issue_type,
    business_area,
    metric_name,
    metric_value,
    CASE
        WHEN metric_value >= 20 THEN 'High'
        WHEN metric_value >= 10 THEN 'Medium'
        ELSE 'Low'
    END AS severity,
    CASE
        WHEN issue_type = 'Warehouse Delay Risk'
            THEN 'Review warehouse operations, labor capacity, and fulfillment bottlenecks.'
        WHEN issue_type = 'Supplier Delay Risk'
            THEN 'Review supplier lead times, supplier risk scores, and backup supplier options.'
        WHEN issue_type = 'Product Stockout Risk'
            THEN 'Review reorder points, demand planning, and inventory replenishment logic.'
    END AS recommended_analysis_action
FROM (
    SELECT * FROM warehouse_delay
    UNION ALL
    SELECT * FROM supplier_delay
    UNION ALL
    SELECT * FROM stockout_risk
) issue_candidates
ORDER BY severity DESC, metric_value DESC;
