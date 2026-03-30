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

