# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to extend the scheduler with priority-based ordering, a next-available-slot capability, and JSON persistence, while keeping the existing tests compatible.

**What did the agent do?**

- Updated [pawpal_system.py](pawpal_system.py) to add a `priority` field to `Task`
- Added `Scheduler.find_next_available_slot()` for advanced scheduling support
- Added `Owner.save_to_json()` and `Owner.load_from_json()` for persistence
- Added regression tests in [tests/test_pawpal.py](tests/test_pawpal.py)
- Helped verify behavior by running pytest after the changes

**What did you have to verify or fix manually?**

I reviewed the generated code to make sure the JSON serialization handled dataclasses correctly and that the new sorting logic matched the intended priority order.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
