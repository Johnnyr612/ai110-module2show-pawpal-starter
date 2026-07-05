from pawpal_system import Pet, Task


def test_task_completion_changes_status():
    task = Task(description="Morning walk", scheduled_time="08:00")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count():
    pet = Pet(name="Mochi", species="dog")

    initial_count = len(pet.tasks)
    pet.add_task(Task(description="Feeding", scheduled_time="18:00"))

    assert len(pet.tasks) == initial_count + 1
