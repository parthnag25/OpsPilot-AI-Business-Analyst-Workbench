import os
import pandas as pd


# ---------------------------------------------------------
# OpsPilot AI: Business Analyst Workflow
# ---------------------------------------------------------
# This script converts SQL-generated issue candidates into
# structured Business Analyst deliverables.
#
# Inputs:
# data/processed/ai_issue_candidates.csv
#
# Outputs:
# data/processed/ai_business_outputs.csv
# ---------------------------------------------------------


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "ai_issue_candidates.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "ai_business_outputs.csv")


def get_stakeholder(issue_type: str) -> str:
    if issue_type == "Product Stockout Risk":
        return "supply chain operations manager"
    if issue_type == "Warehouse Delay Risk":
        return "warehouse operations manager"
    if issue_type == "Supplier Delay Risk":
        return "supplier performance manager"
    return "business stakeholder"


def generate_business_issue_summary(row: pd.Series) -> str:
    return (
        f"{row['business_area']} shows a {row['severity'].lower()} priority "
        f"{row['issue_type'].lower()} with a {row['metric_name']} of "
        f"{row['metric_value']}%. This indicates an operational area that may "
        f"require further business review."
    )


def generate_root_cause_hypothesis(row: pd.Series) -> str:
    issue_type = row["issue_type"]

    if issue_type == "Product Stockout Risk":
        return (
            "The issue may be caused by inaccurate demand planning, reorder points "
            "set too low, supplier replenishment delays, or warehouse-level inventory "
            "planning gaps."
        )

    if issue_type == "Warehouse Delay Risk":
        return (
            "The issue may be caused by warehouse labor constraints, fulfillment "
            "bottlenecks, inventory availability gaps, order processing delays, or "
            "carrier coordination issues."
        )

    if issue_type == "Supplier Delay Risk":
        return (
            "The issue may be caused by supplier lead-time variability, inconsistent "
            "supplier fulfillment, limited backup supplier coverage, or demand pressure "
            "on specific product categories."
        )

    return "The issue may require additional operational review to identify root causes."


def generate_business_requirement(row: pd.Series) -> str:
    issue_type = row["issue_type"]

    if issue_type == "Product Stockout Risk":
        return (
            "The business needs a monitoring process that identifies product categories "
            "with elevated stockout risk and flags them for replenishment review."
        )

    if issue_type == "Warehouse Delay Risk":
        return (
            "The business needs a warehouse performance monitoring process that identifies "
            "locations with elevated late shipment rates and flags them for operational review."
        )

    if issue_type == "Supplier Delay Risk":
        return (
            "The business needs a supplier performance monitoring process that identifies "
            "suppliers with elevated delay rates and flags them for reliability review."
        )

    return "The business needs a structured process to monitor and review operational risks."


def generate_jira_epic(row: pd.Series) -> str:
    issue_type = row["issue_type"]
    business_area = row["business_area"]

    if issue_type == "Product Stockout Risk":
        return f"Improve {business_area} Inventory Availability"

    if issue_type == "Warehouse Delay Risk":
        return f"Reduce Late Shipments at {business_area}"

    if issue_type == "Supplier Delay Risk":
        return f"Improve Delivery Reliability for {business_area}"

    return f"Improve Operational Performance for {business_area}"


def generate_jira_user_story(row: pd.Series) -> str:
    stakeholder = get_stakeholder(row["issue_type"])
    issue_type = row["issue_type"]
    business_area = row["business_area"]

    if issue_type == "Product Stockout Risk":
        return (
            f"As a {stakeholder}, I want to identify {business_area} products with "
            f"high stockout risk so that I can improve replenishment planning and "
            f"reduce missed sales opportunities."
        )

    if issue_type == "Warehouse Delay Risk":
        return (
            f"As a {stakeholder}, I want to monitor late shipment performance at "
            f"{business_area} so that I can identify fulfillment bottlenecks and "
            f"improve delivery reliability."
        )

    if issue_type == "Supplier Delay Risk":
        return (
            f"As a {stakeholder}, I want to track delay performance for {business_area} "
            f"so that I can evaluate supplier reliability and reduce fulfillment risk."
        )

    return (
        f"As a {stakeholder}, I want to monitor {business_area} performance so that "
        f"I can improve operational decision-making."
    )


def generate_acceptance_criteria(row: pd.Series) -> str:
    issue_type = row["issue_type"]

    if issue_type == "Product Stockout Risk":
        criteria = [
            "Stockout rate must be calculated by product category.",
            "Categories above 20% stockout rate must be flagged as high severity.",
            "The output must include metric value, severity, and recommended analyst action.",
            "High-risk categories must require human review before business action."
        ]

    elif issue_type == "Warehouse Delay Risk":
        criteria = [
            "Late shipment rate must be calculated by warehouse.",
            "Warehouses above 10% late shipment rate must be flagged for review.",
            "The output must include metric value, severity, and recommended analyst action.",
            "Warehouse delay recommendations must require human review before business action."
        ]

    elif issue_type == "Supplier Delay Risk":
        criteria = [
            "Supplier delay rate must be calculated by supplier.",
            "Suppliers above 10% delay rate must be flagged for review.",
            "The output must include metric value, severity, and recommended analyst action.",
            "Supplier reliability recommendations must require human review before business action."
        ]

    else:
        criteria = [
            "Operational issue must include a metric value.",
            "Severity must be assigned using defined thresholds.",
            "The output must include a recommended analyst action.",
            "Human review must be required before business action."
        ]

    return " | ".join(criteria)


def generate_executive_recommendation(row: pd.Series) -> str:
    issue_type = row["issue_type"]
    business_area = row["business_area"]

    if issue_type == "Product Stockout Risk":
        return (
            f"Prioritize a review of inventory planning, reorder point logic, and "
            f"replenishment timing for {business_area} to reduce stockout exposure."
        )

    if issue_type == "Warehouse Delay Risk":
        return (
            f"Review warehouse operations, labor capacity, and fulfillment bottlenecks "
            f"at {business_area} to reduce late shipment risk."
        )

    if issue_type == "Supplier Delay Risk":
        return (
            f"Review lead-time reliability, supplier performance patterns, and backup "
            f"supplier options for {business_area}."
        )

    return f"Review operational performance for {business_area}."


def main() -> None:
    print("Running OpsPilot AI Business Analyst workflow...")

    df = pd.read_csv(INPUT_PATH)

    output_rows = []

    for _, row in df.iterrows():
        output_rows.append({
            "issue_type": row["issue_type"],
            "business_area": row["business_area"],
            "metric_name": row["metric_name"],
            "metric_value": row["metric_value"],
            "severity": row["severity"],
            "severity_rank": row["severity_rank"],
            "business_issue_summary": generate_business_issue_summary(row),
            "root_cause_hypothesis": generate_root_cause_hypothesis(row),
            "business_requirement": generate_business_requirement(row),
            "jira_epic": generate_jira_epic(row),
            "jira_user_story": generate_jira_user_story(row),
            "acceptance_criteria": generate_acceptance_criteria(row),
            "executive_recommendation": generate_executive_recommendation(row),
            "human_review_required": True
        })

    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(OUTPUT_PATH, index=False)

    print(f"AI Business Analyst output created: {OUTPUT_PATH}")
    print(f"Total issue records processed: {len(output_df)}")
    print("Workflow complete.")


if __name__ == "__main__":
    main()