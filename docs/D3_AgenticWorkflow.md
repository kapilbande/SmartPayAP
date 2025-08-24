# D3 – Agentic Workflow (LangGraph + Python)

This document describes the D3 deliverable: an agentic workflow that wires the D2 matcher model into a Gen-AI pipeline with human-in-loop approval.

## Workflow Design
1. **Planner** – decides reconciliation steps.
2. **Matcher Tool** – calls the D2 model to predict match/mismatch.
3. **Explainer (LLM)** – generates explanation + vendor email draft.
4. **Human Approval** – mandatory checkpoint before action.

## LangGraph-style Sketch
```text
Planner -> MatcherTool -> ExplainerLLM -> HumanApproval
```
- Match (0) & high confidence → Auto-approve
- Mismatch (1) or low confidence → Explainer + Human approval

## Files
- `scripts/run_workflow.py` – runnable demo workflow
- `src/agent_tools.py` – Matcher & Explainer tool classes
- `docs/D3_AgenticWorkflow.md` – this description
