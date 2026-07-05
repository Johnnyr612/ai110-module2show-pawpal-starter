from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sort_by_time_orders_tasks_by_schedule():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Evening feed", scheduled_time="18:30"))
    pet.add_task(Task(description="Morning walk", scheduled_time="08:00"))
    pet.add_task(Task(description="Afternoon play", scheduled_time="13:00"))

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time()

    assert [task.description for task in ordered] == [
        "Morning walk",
        "Afternoon play",
        "Evening feed",
    ]


def test_filter_tasks_by_status_or_pet_name():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task(description="Morning walk", scheduled_time="08:00"))
    luna.add_task(Task(description="Playtime", scheduled_time="13:00"))
    luna.add_task(Task(description="Medication", scheduled_time="20:00", completed=True))

    scheduler = Scheduler(owner)

    pending_tasks = scheduler.filter_tasks(include_completed=False)
    luna_tasks = scheduler.filter_tasks(pet_name="Luna")

    assert [task.description for task in pending_tasks] == ["Morning walk", "Playtime"]
    assert [task.description for task in luna_tasks] == ["Playtime", "Medication"]


def test_recurring_task_creates_next_occurrence_when_completed():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task = Task(description="Morning walk", scheduled_time="08:00", frequency="daily")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.description == "Morning walk"
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert len(pet.get_tasks()) == 2
