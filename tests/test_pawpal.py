import tempfile
from datetime import date, timedelta
from pathlib import Path

from pawpal_system import Owner, Pet, Scheduler, Task, normalize_time


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


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    first_task = Task(description="Morning walk", scheduled_time="08:00")
    second_task = Task(description="Feeding", scheduled_time="08:00")
    pet.add_task(first_task)
    pet.add_task(second_task)

    scheduler = Scheduler(owner)

    assert scheduler.has_conflicts() is True
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert conflicts[0][0] is first_task
    assert conflicts[0][1] is second_task
    assert "share the same time" in scheduler.get_conflict_warning()


def test_priority_sorting_uses_priority_before_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    low_task = Task(description="Low priority", scheduled_time="08:00", priority="low")
    high_task = Task(description="High priority", scheduled_time="12:00", priority="high")
    medium_task = Task(description="Medium priority", scheduled_time="09:00", priority="medium")
    pet.add_task(low_task)
    pet.add_task(high_task)
    pet.add_task(medium_task)

    scheduler = Scheduler(owner)

    ordered = scheduler.organize_tasks()

    assert [task.description for task in ordered] == [
        "High priority",
        "Medium priority",
        "Low priority",
    ]


def test_find_next_available_slot_returns_first_free_hour():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Morning walk", scheduled_time="08:00"))
    pet.add_task(Task(description="Evening feed", scheduled_time="15:00"))

    scheduler = Scheduler(owner)

    assert scheduler.find_next_available_slot("08:00") == "09:00 AM"


def test_owner_persistence_round_trip():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(description="Feeding", scheduled_time="18:00", priority="high"))

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "data.json"
        owner.save_to_json(str(file_path))
        loaded_owner = Owner.load_from_json(str(file_path))

        assert loaded_owner.name == "Jordan"
        assert loaded_owner.get_pets()[0].name == "Mochi"
        assert loaded_owner.get_all_tasks()[0].description == "Feeding"
        assert loaded_owner.get_all_tasks()[0].priority == "high"


def test_time_normalization_uses_12_hour_format():
    task = Task(description="Feeding", scheduled_time="18:30")

    assert task.scheduled_time == "06:30 PM"
    assert normalize_time("8:45am") == "08:45 AM"


def test_invalid_time_is_rejected():
    task = Task(description="Medication", scheduled_time="13:70 PM")

    assert task.scheduled_time == ""


def test_find_next_available_slot_uses_normalized_12_hour_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(description="Morning walk", scheduled_time="08:00 AM"))
    pet.add_task(Task(description="Evening feed", scheduled_time="03:00 PM"))

    scheduler = Scheduler(owner)

    assert scheduler.find_next_available_slot("08:00 AM") == "09:00 AM"
