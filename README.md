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

## Smarter Scheduling Features

PawPal+ includes intelligent task management and scheduling capabilities:

- **Time-based sorting** (sort_by_time()): Orders tasks chronologically by scheduled time (HH:MM), making it easy to see the day at a glance.
- **Flexible filtering** (filter_tasks()): Filter by completion status (pending/done) and/or pet name to focus on relevant tasks.
- **Auto-recurring tasks** (reschedule_task()): When a daily or weekly task is marked complete, a new instance is automatically created for the next occurrence (using Python's timedelta).
- **Conflict detection** (detect_time_conflicts()): Identifies when multiple tasks are scheduled at the same time and returns warnings, so pet owners can reschedule if needed.
- **Due date tracking**: Each task tracks its due date, enabling smart recurrence logic and timeline visualization.

## Testing PawPal+

### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite includes **11 comprehensive tests** covering:

- **Sorting Correctness** (3 tests): Chronological ordering of tasks by time, handling missing times (pushed to end), and edge-case times (00:00, 23:59)
- **Recurrence Logic** (3 tests): Auto-creation of daily tasks (+1 day), weekly tasks (+7 days), and non-recurring task handling
- **Conflict Detection** (3 tests): Identification of single/multiple time-slot conflicts and validation of conflict-free schedules
- **Core Functionality** (2 tests): Task completion status and pet task management

All tests pass successfully, validating that scheduling, filtering, and recurring task behavior work as designed.

### Confidence Level

**⭐⭐⭐⭐ (4/5 stars)**

**Why:** The test suite validates core scheduling logic, edge cases (missing times, boundary times, non-recurring tasks), and conflict detection. The system handles happy paths reliably. 

**Known limitation:** Conflict detection only flags exact time matches, not overlapping durations—this is a lightweight design tradeoff for MVP performance.

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
