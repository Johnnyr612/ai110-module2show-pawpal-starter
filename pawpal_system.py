from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Owner:
    name: str = ""
    preferences: str = ""
    available_time: int = 0
    preferred_care_times: List[str] = field(default_factory=list)

    def update_preferences(self, preferences: str) -> None:
        pass

    def add_pet(self, pet: "Pet") -> None:
        pass

    def get_available_time(self) -> int:
        return self.available_time


@dataclass
class Pet:
    name: str = ""
    species: str = ""
    age: int = 0
    care_notes: str = ""

    def update_profile(self, name: str | None = None, species: str | None = None, age: int | None = None) -> None:
        pass

    def add_task(self, task: "Task") -> None:
        pass

    def get_care_summary(self) -> str:
        return ""


@dataclass
class Task:
    title: str = ""
    task_type: str = ""
    duration_minutes: int = 0
    priority: str = "medium"
    recurring: bool = False
    preferred_time: str = ""

    def update_priority(self, priority: str) -> None:
        pass

    def update_duration(self, duration_minutes: int) -> None:
        pass

    def mark_completed(self) -> None:
        pass


@dataclass
class DailyPlan:
    date: str = ""
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_planned_time: int = 0
    explanation: str = ""

    def add_task_to_plan(self, task: Task) -> None:
        pass

    def format_plan(self) -> str:
        return ""

    def explain_reasoning(self) -> str:
        return ""


class Scheduler:
    def __init__(self, owner: Owner | None = None, pet: Pet | None = None, tasks: List[Task] | None = None) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks or []
        self.available_time = owner.available_time if owner else 0

    def generate_plan(self) -> DailyPlan:
        return DailyPlan()

    def sort_tasks_by_priority(self) -> List[Task]:
        return list(self.tasks)

    def filter_tasks_by_time(self) -> List[Task]:
        return list(self.tasks)

    def explain_plan(self, plan: DailyPlan) -> str:
        return plan.explanation
