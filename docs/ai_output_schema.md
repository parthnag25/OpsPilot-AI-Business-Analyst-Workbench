# AI Output Schema

## Project: OpsPilot AI

This document defines the structured output schema for the AI-assisted Business Analyst workflow in OpsPilot AI.

The purpose of the AI workflow is to convert SQL-generated operational issue candidates into business analysis deliverables such as issue summaries, root-cause hypotheses, business requirements, Jira-style user stories, acceptance criteria, and executive recommendations.

---

## Input Source

The AI workflow uses structured issue records from the PostgreSQL view:

```sql
opspilot.vw_ai_issue_candidates
