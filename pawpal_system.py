from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str = ""
    scheduled_time: str = ""
    frequency: str = "once"
    completed: bool = False

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
        """Sort tasks by completion status and scheduled time."""
        return sorted(self.get_all_tasks(), key=lambda task: (task.completed, task.scheduled_time))
