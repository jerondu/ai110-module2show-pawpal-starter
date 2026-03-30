# PawPal+ (Module 2 Project)

**PawPal+** is a professional Streamlit web application designed to help pet owners manage and schedule their pets' care tasks efficiently. Built with Python and intelligent algorithms, it transforms chaotic pet care into organized, conflict-free daily schedules.

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

## Features

PawPal+ implements advanced scheduling algorithms to provide a comprehensive pet care management solution:

### 🗂️ **Priority-Based Scheduling**
- **Algorithm**: Tasks are sorted by priority (highest first) using a stable sort that handles `None` priorities gracefully.
- **Benefit**: Ensures critical tasks (e.g., medication) are scheduled before routine ones (e.g., grooming).
- **Implementation**: `Scheduler.prioritize_tasks()` and `Scheduler.generate_schedule()`.

### ⏰ **Time-Based Sorting**
- **Algorithm**: Converts HH:MM time strings to minutes since midnight for accurate chronological ordering. Tasks without times are placed at the end.
- **Benefit**: Provides a natural, time-ordered view of the day's schedule for easy planning.
- **Implementation**: `Scheduler.sort_by_time()` with lambda key conversion.

### 🔍 **Flexible Task Filtering**
- **Algorithm**: Filters tasks by completion status (pending/done) and/or pet name using iterative checks across pets.
- **Benefit**: Allows focused views (e.g., "show only pending tasks for Buddy") without cluttering the interface.
- **Implementation**: `Scheduler.filter_tasks(completed=None, pet_name=None)`.

### 🔄 **Automatic Recurring Tasks**
- **Algorithm**: When a daily/weekly task is completed, creates a new instance with due date advanced by 1 or 7 days using Python's `timedelta`.
- **Benefit**: Eliminates manual re-entry of routine tasks, ensuring consistent care without forgetting.
- **Implementation**: `Scheduler.reschedule_task(task)` with date arithmetic.

### ⚠️ **Conflict Detection**
- **Algorithm**: Groups tasks by exact time slots and flags when multiple tasks share the same time. Lightweight, non-blocking design.
- **Benefit**: Prevents scheduling overlaps, alerting users to potential conflicts for better time management.
- **Implementation**: `Scheduler.detect_time_conflicts()` with hash-based grouping.

### 📅 **Due Date Tracking**
- **Algorithm**: Each task maintains a `due_date` field, enabling timeline-based logic and recurrence calculations.
- **Benefit**: Supports proactive scheduling and overdue task identification.
- **Implementation**: Integrated across `Task` class and scheduling methods.

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

## Architecture

### UML Class Diagram

<a href="/course_images/ai110/uml_final.png" target="_blank"><img src="/course_images/ai110/uml_final.png" alt="UML Class Diagram" /></a>

## 📸 Demo

<a href="/course_images/ai110/working_app.png" target="_blank"><img src="/course_images/ai110/working_app.png" alt="Working App Screenshot" /></a>

## Contributing

This is a Module 2 project. For improvements, consider:
- Adding duration-based conflict detection
- Implementing owner preference constraints
- Enhancing the UI with task editing capabilities

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

### Suggested Workflow

1. Add your owner information and pets
2. Create care tasks with priorities and times
3. Generate schedules and review for conflicts
4. Mark tasks complete to trigger automatic recurrence
