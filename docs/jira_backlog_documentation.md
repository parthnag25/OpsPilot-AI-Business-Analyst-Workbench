# Jira Backlog Documentation

## Project: OpsPilot AI

This document explains how OpsPilot AI converts AI-assisted Business Analyst outputs into a Jira-style backlog.

The Jira backlog is created from SQL-generated operational issue candidates and AI-assisted business analysis outputs. The purpose is to demonstrate how a Business Analyst can move from KPI analysis to structured delivery planning.

---

## Workflow Purpose

The Jira backlog workflow converts business issues into structured user stories that can support project planning, stakeholder review, and implementation discussions.

This workflow demonstrates:

- Jira-style user story creation
- Epic generation
- Acceptance criteria writing
- Priority mapping
- Business area tagging
- Human-in-the-loop review

---

## Input File

The workflow uses the following input file:

```text
data/processed/ai_business_outputs.csv
