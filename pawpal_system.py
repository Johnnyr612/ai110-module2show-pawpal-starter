from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


def _to_minutes(time_value: str) -> int:
    """Convert a time string like 8:30 AM or 18:30 to minutes from midnight."""
    normalized = normalize_time(time_value)
    if not normalized:
        return 24 * 60

    try:
        value = normalized.split(" ")[0]
        hours_str, minutes_str = value.split(":")
        hours = int(hours_str)
        minutes = int(minutes_str)
        meridiem = normalized.split(" ")[1].upper() if len(normalized.split(" ")) > 1 else "AM"
    except (ValueError, IndexError):
        return 24 * 60

    if meridiem == "PM" and hours != 12:
        hours += 12
    elif meridiem == "AM" and hours == 12:
        hours = 0

    if not 0 <= hours <= 23 or not 0 <= minutes <= 59:
        return 24 * 60
    return hours * 60 + minutes


def normalize_time(time_value: str) -> str:
    """Normalize a time string to 12-hour format like 08:30 AM when possible."""
    value = (time_value or "").strip()
    if not value:
        return ""

    normalized_value = value.upper().strip()
    meridiem = ""
    if normalized_value.endswith("AM"):
        meridiem = "AM"
        normalized_value = normalized_value[:-2].strip()
    elif normalized_value.endswith("PM"):
        meridiem = "PM"
        normalized_value = normalized_value[:-2].strip()
    elif "AM" in normalized_value or "PM" in normalized_value:
        return ""

    if not normalized_value:
        return ""

    parts = normalized_value.split(":")
    if len(parts) not in {1, 2} or not parts[0].isdigit():
        return ""

    hours = int(parts[0])
    minutes = 0
    if len(parts) == 2:
        if not parts[1].isdigit():
            return ""
        minutes = int(parts[1])

    if not 0 <= minutes <= 59:
        return ""

    if meridiem:
        if not 1 <= hours <= 12:
            return ""
        return f"{hours:02d}:{minutes:02d} {meridiem}"

    if 0 <= hours <= 23:
        if hours == 0:
            hours = 12
            meridiem = "AM"
        elif hours < 12:
            meridiem = "AM"
        elif hours == 12:
            meridiem = "PM"
        else:
            hours -= 12
            meridiem = "PM"
        return f"{hours:02d}:{minutes:02d} {meridiem}"

    return ""


def _priority_rank(priority: str) -> int:
    """Map a priority label to a sortable number."""
    normalized = priority.lower()
    if normalized == "high":
        return 0
    if normalized == "medium":
        return 1
    return 2


def _format_minutes(minutes: int) -> str:
    """Format minutes from midnight as 12-hour HH:MM AM/PM."""
    hours = minutes // 60
    mins = minutes % 60
    meridiem = "AM"
    if hours >= 12:
        meridiem = "PM"
    display_hours = hours % 12
    if display_hours == 0:
        display_hours = 12
    return f"{display_hours:02d}:{mins:02d} {meridiem}"


@dataclass
class Task:
    description: str = ""
    scheduled_time: str = ""
    frequency: str = "once"
    completed: bool = False
    due_date: date | None = None
    priority: str = "medium"

    def __post_init__(self) -> None:
        """Normalize time and priority values when a task is created."""
        self.scheduled_time = normalize_time(self.scheduled_time)
        normalized_priority = (self.priority or "medium").lower().strip()
        if normalized_priority not in {"low", "medium", "high"}:
            normalized_priority = "medium"
        self.priority = normalized_priority

    def update_description(self, description: str) -> None:
        """Update the task description."""
        self.description = description

    def update_time(self, scheduled_time: str) -> None:
        """Set the task's scheduled time."""
        normalized = normalize_time(scheduled_time)
        self.scheduled_time = normalized if normalized else ""

    def update_frequency(self, frequency: str) -> None:
        """Set how often the task repeats."""
        self.frequency = frequency

    def update_priority(self, priority: str) -> None:
        """Set the task priority level."""
        normalized = priority.lower()
        if normalized not in {"low", "medium", "high"}:
            normalized = "medium"
        self.priority = normalized

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_completed(self) -> None:
        """Alias for marking the task complete."""
        self.mark_complete()

    def mark_pending(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def to_dict(self) -> dict:
        """Convert the task to a JSON-friendly dictionary."""
        return {
            "description": self.description,
            "scheduled_time": self.scheduled_time,
            "frequency": self.frequency,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a task from a JSON-friendly dictionary."""
        due_date = data.get("due_date")
        task = cls(
            description=data.get("description", ""),
            scheduled_time=data.get("scheduled_time", ""),
            frequency=data.get("frequency", "once"),
            completed=data.get("completed", False),
            due_date=date.fromisoformat(due_date) if due_date else None,
            priority=data.get("priority", "medium"),
        )
        return task


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

    def save_to_json(self, file_path: str) -> None:
        """Persist the owner, pets, and tasks to a JSON file."""
        payload = {
            "name": self.name,
            "preferences": self.preferences,
            "pets": [
                {
                    "name": pet.name,
                    "species": pet.species,
                    "age": pet.age,
                    "tasks": [task.to_dict() for task in pet.get_tasks()],
                }
                for pet in self.pets
            ],
        }
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    @classmethod
    def load_from_json(cls, file_path: str) -> "Owner":
        """Load an owner, pets, and tasks from a JSON file."""
        if not os.path.exists(file_path):
            return cls()

        with open(file_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        owner = cls(name=payload.get("name", ""), preferences=payload.get("preferences", ""))
        for pet_data in payload.get("pets", []):
            pet = Pet(
                name=pet_data.get("name", ""),
                species=pet_data.get("species", ""),
                age=pet_data.get("age", 0),
            )
            for task_data in pet_data.get("tasks", []):
                pet.add_task(Task.from_dict(task_data))
            owner.add_pet(pet)
        return owner


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
        """Return all tasks ordered by completion state, priority, time, and description."""
        return sorted(
            self.get_all_tasks(),
            key=lambda task: (
                task.completed,
                _priority_rank(task.priority),
                _to_minutes(task.scheduled_time),
                task.description.lower(),
            ),
        )

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted chronologically by their scheduled HH:MM time."""
        return sorted(self.get_all_tasks(), key=lambda task: _to_minutes(task.scheduled_time))

    def find_next_available_slot(self, preferred_time: str) -> str:
        """Return the first free time slot at or after the preferred time."""
        occupied_slots = {
            _to_minutes(task.scheduled_time)
            for task in self.get_all_tasks()
            if task.scheduled_time
        }
        if not preferred_time:
            preferred_time = "08:00"

        current_minutes = _to_minutes(preferred_time)
        while current_minutes in occupied_slots:
            current_minutes += 60
        return _format_minutes(current_minutes)

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
            priority=task.priority,
        )

        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                pet.add_task(next_task)
                return next_task
        return None
