# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
==================
08:00 | Mochi    | Morning walk
18:30 | Mochi    | Feeding
13:00 | Luna     | Playtime
```


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
(.venv) PS D:\CodePath Forks\Week5-Project2\ai110-module2show-pawpal-starter> python -m pytest
================ test session starts ====================
platform win32 -- Python 3.13.3, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\CodePath Forks\Week5-Project2\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 6 items                                                               

tests\test_pawpal.py ......                                               [100%]

================ 6 passed in 0.02s ======================
```
The tests cover the core scheduler behaviors for PawPal+:

- Task completion state changes
- Adding tasks to a pet
- Sorting tasks by scheduled time
- Filtering tasks by pet and completion status
- Creating the next occurrence of a daily recurring task
- Detecting scheduling conflicts when two tasks share the same time

Confidence Level: (4/5)

The scheduler behavior is well covered by the current test suite, and the recent pytest run showed 6 passing tests. The implementation is good but there is still room for more test cases.

## 📐 Smarter Scheduling

The scheduler now supports several core behaviors for organizing pet-care tasks:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority-based ordering | `Scheduler.organize_tasks()` | Tasks are sorted by completion status, priority level, and scheduled time. |
| Next available slot | `Scheduler.find_next_available_slot()` | The scheduler suggests the first open time slot after a preferred time. |
| Filtering | `Scheduler.filter_tasks()` | Tasks can be filtered by pet name and whether completed tasks should be included. |
| Conflict handling | `Scheduler.detect_conflicts()` and `Scheduler.get_conflict_warning()` | The scheduler identifies overlapping task times and returns a lightweight warning message. |
| Recurring tasks | `Scheduler.handle_recurring_tasks()` and `Scheduler.complete_task()` | Daily and weekly tasks can be marked as recurring, and completing one creates the next occurrence automatically. |

## 💾 Data Persistence

PawPal+ now saves owner, pet, and task data between runs using a JSON file.

### Persistence workflow

1. When the app or backend saves data, it writes the current state to `data.json`.
2. On the next run, the app can reload that file through `Owner.load_from_json()`.
3. This keeps pets and tasks available across sessions without manually re-entering them.

### Files updated for persistence

- [pawpal_system.py](pawpal_system.py) — added `Owner.save_to_json()` and `Owner.load_from_json()` plus JSON-safe task serialization
- [tests/test_pawpal.py](tests/test_pawpal.py) — added tests covering persistence and scheduler enhancements

### Example CLI output

```text
Today's Schedule
==================
08:00 | Mochi | Medication (High)
09:00 | Mochi | Feeding (Medium)
18:00 | Mochi | Grooming (Low)
```

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter owner name(Johnny) and `Save Owner`.
2. Enter Dexter name for dog pet and press `add pet`.
3. Add task by selecting pet name.
4. Include task title and task frequency then press `Add Task`.
5. Then press `Generate Schedule` to check for scheduling conflicts, sort by name, and display schedule for tasks.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
