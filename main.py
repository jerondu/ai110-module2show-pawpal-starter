from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

if __name__ == "__main__":
    owner = Owner(name="Jessica", email="jessica@example.com", preferences={"work_hours": "9-17"})

    pet1 = Pet(name="Milo", type="Cat", age=3)
    pet2 = Pet(name="Buddy", type="Dog", age=5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Define today's date
    today = datetime.now().date()

    # Add tasks with due dates out of order
    task1 = Task(
        description="Feed Milo", 
        duration=10, 
        frequency="daily", 
        priority=2, 
        time="09:00",
        due_date=today
    )
    task2 = Task(
        description="Walk Buddy", 
        duration=30, 
        frequency="daily", 
        priority=3, 
        time="09:00",  # CONFLICT: Same time as Feed Milo
        due_date=today
    )
    task3 = Task(
        description="Give Milo medication", 
        duration=5, 
        frequency="daily", 
        priority=1, 
        time="14:00",
        due_date=today
    )
    task4 = Task(
        description="Groom Buddy", 
        duration=45, 
        frequency="weekly", 
        priority=2, 
        time="10:00",
        due_date=today
    )
    task5 = Task(
        description="Clean litter box", 
        duration=15, 
        frequency="daily", 
        priority=3, 
        time="09:00",  # CONFLICT: Also at 09:00 with Feed Milo and Walk Buddy
        due_date=today
    )
    
    task6 = Task(
        description="Brush Buddy's coat",
        duration=20,
        frequency="weekly",
        priority=2,
        time="14:00",  # CONFLICT: Same time as Give Milo medication
        due_date=today
    )

    # Add tasks to pets
    pet1.add_care_need(task1)
    pet1.add_care_need(task3)
    pet1.add_care_need(task5)
    pet2.add_care_need(task2)
    pet2.add_care_need(task4)
    pet2.add_care_need(task6)

    scheduler = Scheduler(owner=owner)

    print("=" * 80)
    print("ALL TASKS WITH SCHEDULED TIMES")
    print("=" * 80)
    all_tasks = scheduler.retrieve_all_tasks()
    for t in all_tasks:
        status = "✓ Done" if t.completed else "○ Pending"
        due = f"{t.due_date}" if t.due_date else "N/A"
        print(f"- {status:10} | {t.description:25} | Time: {t.time:5} | Due: {due:12}")

    print("\n" + "=" * 80)
    print("CONFLICT DETECTION")
    print("=" * 80)
    conflicts = scheduler.detect_time_conflicts()
    if conflicts:
        print("⚠️  SCHEDULING CONFLICTS DETECTED:\n")
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("✓ No scheduling conflicts detected.")

    print("\n" + "=" * 80)
    print("TASKS SORTED BY TIME (showing conflicts)")
    print("=" * 80)
    by_time = scheduler.sort_by_time()
    for t in by_time:
        status = "✓ Done" if t.completed else "○ Pending"
        print(f"- {status:10} | {t.description:25} | Time: {t.time if t.time else 'N/A':5}")

    print("\n" + "=" * 80)
    print("COMPLETING TASKS & AUTO-GENERATING RECURRING INSTANCES")
    print("=" * 80)

    # Mark task1 (daily Feed Milo) as complete - should create new instance for tomorrow
    print(f"\n→ Completing: '{task1.description}' (daily, due {task1.due_date})")
    scheduler.complete_task(task1)
    new_task1 = scheduler.reschedule_task(task1)
    if new_task1:
        print(f"  ✓ New instance created: due {new_task1.due_date} ({new_task1.due_date - today}) day(s) from today")

    # Mark task2 (daily Walk Buddy) as complete - should create new instance for tomorrow
    print(f"\n→ Completing: '{task2.description}' (daily, due {task2.due_date})")
    scheduler.complete_task(task2)
    new_task2 = scheduler.reschedule_task(task2)
    if new_task2:
        print(f"  ✓ New instance created: due {new_task2.due_date} ({new_task2.due_date - today}) day(s) from today")

    # Mark task4 (weekly Groom Buddy) as complete - should create new instance for next week
    print(f"\n→ Completing: '{task4.description}' (weekly, due {task4.due_date})")
    scheduler.complete_task(task4)
    new_task4 = scheduler.reschedule_task(task4)
    if new_task4:
        print(f"  ✓ New instance created: due {new_task4.due_date} ({new_task4.due_date - today}) day(s) from today")

    print("\n" + "=" * 80)
    print("ALL TASKS AFTER RESCHEDULING (including new recurring instances)")
    print("=" * 80)
    all_tasks_updated = scheduler.retrieve_all_tasks()
    for t in all_tasks_updated:
        status = "✓ Done" if t.completed else "○ Pending"
        due = f"{t.due_date}" if t.due_date else "N/A"
        print(f"- {status:10} | {t.description:25} | Time: {t.time if t.time else 'N/A':5} | Due: {due:12}")

    print("\n" + "=" * 80)
    print("CONFLICTS AFTER RESCHEDULING")
    print("=" * 80)
    conflicts_after = scheduler.detect_time_conflicts()
    if conflicts_after:
        print("⚠️  SCHEDULING CONFLICTS STILL PRESENT:\n")
        for warning in conflicts_after:
            print(f"  {warning}")
    else:
        print("✓ No scheduling conflicts detected.")

    print("\n" + "=" * 80)
    print("PENDING TASKS ONLY (Ready to schedule for today/future)")
    print("=" * 80)
    pending = scheduler.filter_tasks(completed=False)
    for t in pending:
        due = f"{t.due_date}" if t.due_date else "N/A"
        print(f"- {t.description:25} | Time: {t.time if t.time else 'N/A':5} | Due: {due:12} | Priority: {t.priority}")



