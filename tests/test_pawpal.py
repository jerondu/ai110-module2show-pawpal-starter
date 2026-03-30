from pawpal_system import Task, Pet


def test_task_completion_changes_status():
    task = Task(description="Feed pet", duration=10, frequency="daily", priority=1)
    assert not task.completed

    task.mark_complete()
    assert task.completed


def test_pet_task_addition_increments_count():
    pet = Pet(name="Milo", type="Cat", age=3)
    assert len(pet.care_needs) == 0

    task = Task(description="Give pills", duration=5, frequency="daily", priority=2)
    pet.add_care_need(task)
    assert len(pet.care_needs) == 1


def test_scheduler_sort_by_time():
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    task1 = Task(description="Brush", duration=10, frequency="daily", time="15:30")
    task2 = Task(description="Feed", duration=5, frequency="daily", time="08:00")
    task3 = Task(description="Walk", duration=20, frequency="daily", time="12:15")

    owner.add_pet(Pet(name="Milo", type="Cat", age=3))
    owner.pets[0].add_care_need(task1)
    owner.pets[0].add_care_need(task2)
    owner.pets[0].add_care_need(task3)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [t.description for t in sorted_tasks] == ["Feed", "Walk", "Brush"]


def test_sort_by_time_with_missing_times():
    """Sorting Correctness: Tasks without times should be pushed to end."""
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    task1 = Task(description="Feed", duration=5, frequency="daily", time="09:00")
    task2 = Task(description="Play", duration=15, frequency="daily")  # No time
    task3 = Task(description="Walk", duration=20, frequency="daily", time="14:00")

    owner.add_pet(Pet(name="Buddy", type="Dog", age=4))
    owner.pets[0].add_care_need(task1)
    owner.pets[0].add_care_need(task2)
    owner.pets[0].add_care_need(task3)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()

    # Tasks with times come first (chronological), then tasks without times
    assert sorted_tasks[0].description == "Feed"  # 09:00
    assert sorted_tasks[1].description == "Walk"  # 14:00
    assert sorted_tasks[2].description == "Play"  # No time (end)


def test_sort_by_time_edge_times():
    """Sorting Correctness: Edge case times (00:00 and 23:59) sort correctly."""
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    task1 = Task(description="Evening", duration=10, frequency="daily", time="23:59")
    task2 = Task(description="Morning", duration=10, frequency="daily", time="00:00")
    task3 = Task(description="Noon", duration=10, frequency="daily", time="12:00")

    owner.add_pet(Pet(name="Max", type="Cat", age=2))
    owner.pets[0].add_care_need(task1)
    owner.pets[0].add_care_need(task2)
    owner.pets[0].add_care_need(task3)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [t.description for t in sorted_tasks] == ["Morning", "Noon", "Evening"]


def test_recurrence_logic_daily_task():
    """Recurrence Logic: Marking a daily task complete creates new task for tomorrow."""
    from pawpal_system import Scheduler, Owner
    from datetime import datetime, timedelta

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    today = datetime.now().date()
    
    task = Task(
        description="Feed Milo", 
        duration=10, 
        frequency="daily", 
        priority=2,
        time="09:00",
        due_date=today
    )

    owner.add_pet(Pet(name="Milo", type="Cat", age=3))
    owner.pets[0].add_care_need(task)

    scheduler = Scheduler(owner=owner)
    
    # Complete the task
    scheduler.complete_task(task)
    assert task.completed is True
    
    # Reschedule should create new instance for tomorrow
    new_task = scheduler.reschedule_task(task)
    assert new_task is not None
    assert new_task.description == "Feed Milo"
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False
    assert new_task.frequency == "daily"


def test_recurrence_logic_weekly_task():
    """Recurrence Logic: Marking a weekly task complete creates new task for next week."""
    from pawpal_system import Scheduler, Owner
    from datetime import datetime, timedelta

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    today = datetime.now().date()
    
    task = Task(
        description="Groom Buddy", 
        duration=45, 
        frequency="weekly", 
        priority=2,
        time="10:00",
        due_date=today
    )

    owner.add_pet(Pet(name="Buddy", type="Dog", age=5))
    owner.pets[0].add_care_need(task)

    scheduler = Scheduler(owner=owner)
    
    # Complete the task
    scheduler.complete_task(task)
    assert task.completed is True
    
    # Reschedule should create new instance for next week (7 days)
    new_task = scheduler.reschedule_task(task)
    assert new_task is not None
    assert new_task.description == "Groom Buddy"
    assert new_task.due_date == today + timedelta(days=7)
    assert new_task.completed is False
    assert new_task.frequency == "weekly"


def test_recurrence_logic_one_time_task():
    """Recurrence Logic: One-time (non-recurring) tasks should not be rescheduled."""
    from pawpal_system import Scheduler, Owner
    from datetime import datetime

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    today = datetime.now().date()
    
    task = Task(
        description="Vet checkup", 
        duration=30, 
        frequency="once", 
        priority=3,
        due_date=today
    )

    owner.add_pet(Pet(name="Max", type="Cat", age=2))
    owner.pets[0].add_care_need(task)

    scheduler = Scheduler(owner=owner)
    
    # Complete the task
    scheduler.complete_task(task)
    
    # Reschedule should return None for non-recurring tasks
    new_task = scheduler.reschedule_task(task)
    assert new_task is None


def test_conflict_detection_two_tasks_same_time():
    """Conflict Detection: Scheduler flags when two tasks are at the same time."""
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    
    task1 = Task(description="Feed Milo", duration=10, frequency="daily", time="09:00")
    task2 = Task(description="Walk Buddy", duration=30, frequency="daily", time="09:00")

    owner.add_pet(Pet(name="Milo", type="Cat", age=3))
    owner.pets[0].add_care_need(task1)
    
    owner.add_pet(Pet(name="Buddy", type="Dog", age=5))
    owner.pets[1].add_care_need(task2)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_time_conflicts()

    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]
    assert "2 tasks" in conflicts[0]


def test_conflict_detection_multiple_conflicts():
    """Conflict Detection: Scheduler identifies multiple separate time conflicts."""
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    
    task1 = Task(description="Feed Milo", duration=10, frequency="daily", time="09:00")
    task2 = Task(description="Clean litter", duration=15, frequency="daily", time="09:00")
    task3 = Task(description="Medication", duration=5, frequency="daily", time="14:00")
    task4 = Task(description="Walk Buddy", duration=30, frequency="daily", time="14:00")

    owner.add_pet(Pet(name="Milo", type="Cat", age=3))
    owner.pets[0].add_care_need(task1)
    owner.pets[0].add_care_need(task2)
    owner.pets[0].add_care_need(task3)
    
    owner.add_pet(Pet(name="Buddy", type="Dog", age=5))
    owner.pets[1].add_care_need(task4)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_time_conflicts()

    assert len(conflicts) == 2
    # Check for both time slots in conflict warnings
    time_slots = [c for c in conflicts if "09:00" in c or "14:00" in c]
    assert len(time_slots) == 2


def test_conflict_detection_no_conflicts():
    """Conflict Detection: Scheduler returns empty list when no conflicts exist."""
    from pawpal_system import Scheduler, Owner

    owner = Owner(name="Jess", email="jess@example.com", preferences={})
    
    task1 = Task(description="Feed Milo", duration=10, frequency="daily", time="09:00")
    task2 = Task(description="Walk Buddy", duration=30, frequency="daily", time="14:00")
    task3 = Task(description="Playtime", duration=15, frequency="daily", time="16:00")

    owner.add_pet(Pet(name="Milo", type="Cat", age=3))
    owner.pets[0].add_care_need(task1)
    
    owner.add_pet(Pet(name="Buddy", type="Dog", age=5))
    owner.pets[1].add_care_need(task2)
    owner.pets[1].add_care_need(task3)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_time_conflicts()

    assert len(conflicts) == 0
    assert conflicts == []


