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
