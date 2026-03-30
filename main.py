from pawpal_system import Owner, Pet, Task, Scheduler

if __name__ == "__main__":
    owner = Owner(name="Jessica", email="jessica@example.com", preferences={"work_hours": "9-17"})

    pet1 = Pet(name="Milo", type="Cat", age=3)
    pet2 = Pet(name="Buddy", type="Dog", age=5)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(description="Feed Milo", duration=10, frequency="daily", priority=2)
    task2 = Task(description="Walk Buddy", duration=30, frequency="daily", priority=3)
    task3 = Task(description="Give Milo medication", duration=5, frequency="daily", priority=1)

    pet1.add_care_need(task1)
    pet1.add_care_need(task3)
    pet2.add_care_need(task2)

    scheduler = Scheduler(owner=owner)
    today_schedule = scheduler.generate_schedule(date="2026-03-29")

    print("Today's Schedule")
    print("===============")
    for t in today_schedule.tasks:
        status = "Done" if t.completed else "Pending"
        print(f"- {t.description} ({t.duration} min, freq={t.frequency}, priority={t.priority}) -> {status}")
