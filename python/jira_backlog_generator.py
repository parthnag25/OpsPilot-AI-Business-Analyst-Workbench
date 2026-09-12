import os
import pandas as pd


# ---------------------------------------------------------
# OpsPilot AI: Jira Backlog Generator
# ---------------------------------------------------------
# This script converts AI Business Analyst outputs into a
# Jira-style backlog CSV.
#
# Input:
# data/processed/ai_business_outputs.csv
# Output:
# jira/jira_user_stories.csv
# ---------------------------------------------------------


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "ai_business_outputs.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "jira")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "jira_user_stories.csv")


def map_priority(severity: str) -> str:
    if severity == "High":
        return "High"
    if severity == "Medium":
        return "Medium"
    return "Low"


def create_issue_key(index: int) -> str:
    return f"OPSPILOT-{index + 1}"


def create_summary(row: pd.Series) -> str:
    return f"{row['issue_type']}: {row['business_area']} - {row['metric_value']}%"


def create_labels(row: pd.Series) -> str:
    issue_type = row["issue_type"]

    if issue_type == "Product Stockout Risk":
        return "inventory,stockout,supply-chain,ai-generated"

    if issue_type == "Warehouse Delay Risk":
        return "warehouse,late-shipments,operations,ai-generated"

    if issue_type == "Supplier Delay Risk":
        return "supplier-risk,delivery-delay,procurement,ai-generated"

    return "business-analysis,ai-generated"


def main() -> None:
    print("Generating OpsPilot AI Jira-style backlog...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    backlog_rows = []

    for index, row in df.iterrows():
        backlog_rows.append({
            "issue_key": create_issue_key(index),
            "issue_type": "Story",
            "summary": create_summary(row),
            "epic_name": row["jira_epic"],
            "user_story": row["jira_user_story"],
            "acceptance_criteria": row["acceptance_criteria"],
            "priority": map_priority(row["severity"]),
            "status": "To Do",
            "labels": create_labels(row),
            "business_area": row["business_area"],
            "metric_name": row["metric_name"],
            "metric_value": row["metric_value"],
            "severity": row["severity"],
            "human_review_required": row["human_review_required"]
        })

    backlog_df = pd.DataFrame(backlog_rows)
    backlog_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Jira-style backlog created: {OUTPUT_PATH}")
    print(f"Total Jira stories created: {len(backlog_df)}")
    print("Backlog generation complete.")


if __name__ == "__main__":
    main()