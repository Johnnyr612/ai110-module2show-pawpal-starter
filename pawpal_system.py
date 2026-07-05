from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


def _to_minutes(time_value: str) -> int:
    """Convert a HH:MM time string to minutes from midnight."""
    try:
        hours, minutes = map(int, time_value.split(":"))
        return hours * 60 + minutes
    except ValueError:
        return 24 * 60


@dataclass
class Task:
    description: str = ""
    scheduled_time: str = ""
    frequency: str = "once"
    completed: bool = False
    due_date: date | None = None

    def update_description(self, description: str) -> None:
        """Update the task description."""
        self.description = description

    def update_time(self, scheduled_time: str) -> None:
        """Set the task's scheduled time."""
        self.scheduled_time = scheduled_time

    def update_frequency(self, frequency: str) -> None:
        """Set how often the task repeats."""
        self.frequency = frequency

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_completed(self) -> None:
        """Alias for marking the task complete."""
        self.mark_complete()

    def mark_pending(self) -> None:
        """Mark the task as not completed."""
        self.completed = False


@dataclass
class Pet:
    name: str = ""
    species: str = ""
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def update_profile(self, name: str | None = None, species: str | None = None, age: int | None = None) -> None:
        """Update the pet's profile information."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to the pet."""
        return list(self.tasks)

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for the pet."""
        return [task for task in self.tasks if not task.completed]

    def get_care_summary(self) -> str:
        """Return a short summary of the pet."""
        return f"{self.name} the {self.species}"


@dataclass
class Owner:
    name: str = ""
    preferences: str = ""
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, preferences: str) -> None:
        """Update the owner's care preferences."""
        self.preferences = preferences

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by the owner."""
        return list(self.pets)

    def get_all_tasks(self) -> List[Task]:
        """Collect all tasks from every pet owned by the owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across the owner's pets."""
        return [task for task in self.get_all_tasks() if not task.completed]


class Scheduler:
    def __init__(self, owner: Owner | None = None) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return every task from the owner's pets."""
        if self.owner is None:
            return []
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for the owner."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def organize_tasks(self) -> List[Task]:
        """Return all tasks ordered by completion state, time, and description."""
        return sorted(
            self.get_all_tasks(),
            key=lambda task: (task.completed, _to_minutes(task.scheduled_time), task.description.lower()),
        )

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted chronologically by their scheduled HH:MM time."""
        return sorted(self.get_all_tasks(), key=lambda task: _to_minutes(task.scheduled_time))

    def filter_tasks(self, pet_name: str | None = None, include_completed: bool = True) -> List[Task]:
        """Return tasks filtered by pet name and whether completed items should be included."""
        tasks = self.get_all_tasks()
        if pet_name:
            tasks = [task for task in tasks if self._task_belongs_to_pet(task, pet_name)]
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        return tasks

    def _task_belongs_to_pet(self, task: Task, pet_name: str) -> bool:
        """Return True when a task is assigned to the pet with the given name."""
        if self.owner is None:
            return False
        return any(task in pet.get_tasks() and pet.name == pet_name for pet in self.owner.get_pets())

    def has_conflicts(self) -> bool:
        """Return True if any two tasks share the same scheduled time slot."""
        seen_times: set[str] = set()
        for task in self.get_all_tasks():
            if task.scheduled_time and task.scheduled_time in seen_times:
                return True
            if task.scheduled_time:
                seen_times.add(task.scheduled_time)
        return False

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of tasks that overlap because they share the same time."""
        conflicts: list[tuple[Task, Task]] = []
        seen: list[Task] = []
        for task in self.get_all_tasks():
            if not task.scheduled_time:
                continue
            for prior in seen:
                if prior.scheduled_time == task.scheduled_time:
                    conflicts.append((prior, task))
            seen.append(task)
        return conflicts

    def get_conflict_warning(self) -> str:
        """Return a user-friendly warning for the first detected scheduling conflict."""
        conflicts = self.detect_conflicts()
        if not conflicts:
            return "No scheduling conflicts detected."

        first, second = conflicts[0]
        return (
            f"Warning: tasks '{first.description}' and '{second.description}' share the same time "
            f"({first.scheduled_time})."
        )

    def handle_recurring_tasks(self) -> List[Task]:
        """Return tasks that repeat on a daily or weekly schedule."""
        return [task for task in self.get_all_tasks() if task.frequency != "once"]

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and create the next recurring instance for daily or weekly tasks."""
        task.mark_complete()
        if task.frequency not in {"daily", "weekly"}:
            return None

        if self.owner is None:
            return None

        next_due_date = task.due_date + timedelta(days=1 if task.frequency == "daily" else 7) if task.due_date else date.today() + timedelta(days=1 if task.frequency == "daily" else 7)
        next_task = Task(
            description=task.description,
            scheduled_time=task.scheduled_time,
            frequency=task.frequency,
            completed=False,
            due_date=next_due_date,
        )

        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                pet.add_task(next_task)
                return next_task
        return None
