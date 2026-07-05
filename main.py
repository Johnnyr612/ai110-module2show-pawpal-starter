from pawpal_system import Owner, Pet, Scheduler, Task


def build_sample_schedule() -> Owner:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=2)

    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task(description="Feeding", scheduled_time="18:30", frequency="daily"))
    mochi.add_task(Task(description="Morning walk", scheduled_time="08:00", frequency="daily"))
    luna.add_task(Task(description="Playtime", scheduled_time="13:00", frequency="daily"))
    luna.add_task(Task(description="Medication", scheduled_time="20:00", frequency="once", completed=True))
    mochi.add_task(Task(description="Vet visit", scheduled_time="13:00", frequency="once"))

    return owner


def print_schedule(owner: Owner) -> None:
    scheduler = Scheduler(owner=owner)
    tasks = scheduler.sort_by_time()
    pending_tasks = scheduler.filter_tasks(include_completed=False)
    luna_tasks = scheduler.filter_tasks(pet_name="Luna")

    print("Today's Schedule")
    print("=" * 18)
    for task in tasks:
        pet_name = next(pet.name for pet in owner.get_pets() if task in pet.get_tasks())
        print(f"{task.scheduled_time} | {pet_name:<8} | {task.description}")

    print("\nPending tasks:")
    for task in pending_tasks:
        print(f"- {task.description}")

    print("\nLuna tasks:")
    for task in luna_tasks:
        print(f"- {task.description}")

    print("\nConflict check:")
    print(scheduler.get_conflict_warning())


if __name__ == "__main__":
    owner = build_sample_schedule()
    print_schedule(owner)
