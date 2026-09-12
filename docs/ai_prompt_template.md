# AI Prompt Template

## Project: OpsPilot AI

This document defines the prompt template used by the AI-assisted Business Analyst workflow.

The prompt converts SQL-generated operational issue candidates into structured Business Analyst outputs, including issue summaries, root-cause hypotheses, business requirements, Jira-style user stories, acceptance criteria, and executive recommendations.

---

## Prompt Purpose

The AI prompt is designed to act as a Business Analyst assistant.

It should not make final business decisions. Its role is to help structure analysis outputs so that a human analyst can review, refine, and approve them.

---

## Input Fields

The prompt will receive the following fields from the PostgreSQL view:

```sql
opspilot.vw_ai_issue_candidates
