from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Task:
    description: str
    duration: int
    frequency: str
    completed: bool = False
    priority: Optional[int] = None

    def get_description(self) -> str:
        """Return task description."""
        return self.description

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_due(self) -> bool:
        """Return True if task is not completed."""
        return not self.completed

@dataclass
class Schedule:
    date: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to the schedule."""
        self.tasks.append(task)

    def complete_task(self, task: Task):
        """Mark a schedule task as completed if present."""
        if task in self.tasks:
            task.mark_complete()

@dataclass
class Pet:
    name: str
    type: str
    age: int
    care_needs: List[Task] = field(default_factory=list)

    def add_care_need(self, task: Task):
        """Add a care task to this pet."""
        self.care_needs.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all care tasks for this pet."""
        return self.care_needs

    def remove_task(self, task: Task):
        """Remove a task from this pet if it exists."""
        if task in self.care_needs:
            self.care_needs.remove(task)

class Owner:
    def __init__(self, name: str, email: str, preferences: Dict):
        self.name = name
        self.email = email
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets for this owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def update_preferences(self, prefs: Dict):
        """Update owner preferences with new values."""
        self.preferences.update(prefs)

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.constraints = owner.preferences

    def retrieve_all_tasks(self) -> List[Task]:
        """Fetch all tasks for the owner from all pets."""
        return self.owner.get_all_tasks()

    def prioritize_tasks(self) -> List[Task]:
        """Return tasks sorted by priority, highest first."""
        tasks = self.retrieve_all_tasks()
        return sorted(tasks, key=lambda t: (t.priority is None, t.priority), reverse=True)

    def generate_schedule(self, date: str) -> Schedule:
        """Create schedule for a given date, including due tasks."""
        tasks = self.prioritize_tasks()
        schedule = Schedule(date=date)
        for task in tasks:
            if task.is_due():
                schedule.add_task(task)
        return schedule

    def complete_task(self, task: Task):
        """Mark a given task as complete."""
        task.mark_complete()
