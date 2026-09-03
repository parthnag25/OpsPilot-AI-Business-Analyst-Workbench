-- =========================================================
-- OpsPilot AI: PostgreSQL Table Creation Script
-- Project: Agentic Business Analyst Workbench
-- Purpose: Create database schema and tables for supply chain analytics
-- =========================================================

CREATE SCHEMA IF NOT EXISTS opspilot;

-- Drop fact tables first because they depend on dimension tables
DROP TABLE IF EXISTS opspilot.fact_returns;
DROP TABLE IF EXISTS opspilot.fact_inventory;
DROP TABLE IF EXISTS opspilot.fact_shipments;
DROP TABLE IF EXISTS opspilot.fact_orders;

-- Drop dimension tables
DROP TABLE IF EXISTS opspilot.dim_customer;
DROP TABLE IF EXISTS opspilot.dim_warehouse;
DROP TABLE IF EXISTS opspilot.dim_product;
DROP TABLE IF EXISTS opspilot.dim_supplier;
DROP TABLE IF EXISTS opspilot.dim_date;

-- =========================================================
-- Dimension Tables
-- =========================================================

CREATE TABLE opspilot.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week_number INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL
);

CREATE TABLE opspilot.dim_supplier (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    supplier_region VARCHAR(50) NOT NULL,
    standard_lead_time_days INTEGER NOT NULL,
    supplier_risk_score INTEGER NOT NULL
);

CREATE TABLE opspilot.dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(75) NOT NULL,
    subcategory VARCHAR(75) NOT NULL,
    unit_cost NUMERIC(12, 2) NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    supplier_id VARCHAR(20) NOT NULL,
    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES opspilot.dim_supplier(supplier_id)
);

CREATE TABLE opspilot.dim_warehouse (
    warehouse_id VARCHAR(20) PRIMARY KEY,
    warehouse_name VARCHAR(150) NOT NULL,
    region VARCHAR(50) NOT NULL,
    state VARCHAR(10) NOT NULL,
    capacity_units INTEGER NOT NULL,
    labor_hours_available INTEGER NOT NULL
);

CREATE TABLE opspilot.dim_customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_segment VARCHAR(50) NOT NULL,
    state VARCHAR(10) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- =========================================================
-- Fact Tables
-- =========================================================

CREATE TABLE opspilot.fact_orders (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    warehouse_id VARCHAR(20) NOT NULL,
    quantity_ordered INTEGER NOT NULL,
    order_value NUMERIC(12, 2) NOT NULL,
    promised_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    order_status VARCHAR(30) NOT NULL,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES opspilot.dim_customer(customer_id),
    CONSTRAINT fk_orders_product
        FOREIGN KEY (product_id)
        REFERENCES opspilot.dim_product(product_id),
    CONSTRAINT fk_orders_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES opspilot.dim_warehouse(warehouse_id)
);

CREATE TABLE opspilot.fact_shipments (
    shipment_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    carrier VARCHAR(50) NOT NULL,
    shipping_method VARCHAR(50) NOT NULL,
    shipping_cost NUMERIC(12, 2) NOT NULL,
    delay_days INTEGER NOT NULL,
    delay_reason VARCHAR(75) NOT NULL,
    CONSTRAINT fk_shipments_orders
        FOREIGN KEY (order_id)
        REFERENCES opspilot.fact_orders(order_id)
);

CREATE TABLE opspilot.fact_inventory (
    inventory_id VARCHAR(20) PRIMARY KEY,
    date_key INTEGER NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    warehouse_id VARCHAR(20) NOT NULL,
    opening_stock INTEGER NOT NULL,
    closing_stock INTEGER NOT NULL,
    reorder_point INTEGER NOT NULL,
    stockout_flag BOOLEAN NOT NULL,
    CONSTRAINT fk_inventory_date
        FOREIGN KEY (date_key)
        REFERENCES opspilot.dim_date(date_key),
    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES opspilot.dim_product(product_id),
    CONSTRAINT fk_inventory_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES opspilot.dim_warehouse(warehouse_id)
);

CREATE TABLE opspilot.fact_returns (
    return_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    return_date DATE NOT NULL,
    return_reason VARCHAR(100) NOT NULL,
    return_cost NUMERIC(12, 2) NOT NULL,
    CONSTRAINT fk_returns_orders
        FOREIGN KEY (order_id)
        REFERENCES opspilot.fact_orders(order_id),
    CONSTRAINT fk_returns_product
        FOREIGN KEY (product_id)
        REFERENCES opspilot.dim_product(product_id)
);

-- =========================================================
-- Basic Validation Query
-- =========================================================

SELECT 'OpsPilot AI tables created successfully' AS status;
