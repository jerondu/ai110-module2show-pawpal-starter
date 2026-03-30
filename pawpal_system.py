from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta

@dataclass
class Task:
    description: str
    duration: int
    frequency: str
    time: Optional[str] = None  # HH:MM format for scheduled time
    due_date: Optional[datetime.date] = None  # Track when task is due
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

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks chronologically by scheduled time (HH:MM format).
        
        Converts time strings to minutes since midnight for accurate sorting.
        Tasks without a scheduled time are placed at the end (infinity value).
        
        Args:
            tasks: List of tasks to sort. If None, retrieves all tasks from owner.
        
        Returns:
            Sorted list of tasks ordered by time (earliest first).
        
        Example:
            sorted_tasks = scheduler.sort_by_time()
            # Returns tasks ordered 07:30 -> 09:00 -> 14:00 -> 18:00
        """
        if tasks is None:
            tasks = self.retrieve_all_tasks()

        def _time_key(task: Task):
            # support tasks without time by pushing to end
            if not task.time:
                return float('inf')
            hh, mm = task.time.split(":")
            return int(hh) * 60 + int(mm)

        return sorted(tasks, key=_time_key)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.
        
        Supports flexible filtering on task state and pet ownership. Both parameters
        are optional; omit for no filtering or combine for precise task selection.
        
        Args:
            completed: True for completed tasks, False for pending, None for all (default)
            pet_name: Filter by specific pet name (e.g., 'Buddy'), None for all pets (default)
        
        Returns:
            List of filtered tasks matching all specified criteria.
        
        Example:
            pending = scheduler.filter_tasks(completed=False)
            buddy_tasks = scheduler.filter_tasks(pet_name='Buddy')
            buddy_pending = scheduler.filter_tasks(completed=False, pet_name='Buddy')
        """
        filtered_tasks: List[Task] = []
        
        for pet in self.owner.get_all_pets():
            # Skip if filtering by pet_name and this is not the target pet
            if pet_name and pet.name != pet_name:
                continue
            
            for task in pet.get_tasks():
                # Apply completion status filter
                if completed is not None and task.completed != completed:
                    continue
                filtered_tasks.append(task)
        
        return filtered_tasks

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

    def reschedule_task(self, task: Task) -> Optional[Task]:
        """Auto-generate next occurrence of a completed recurring task.
        
        When a recurring task is marked complete, this method creates a new instance
        with an updated due date. Daily tasks advance by 1 day; weekly tasks by 7 days.
        New task is automatically added to the pet that owns the original task.
        
        Args:
            task: The completed recurring task to reschedule
        
        Returns:
            New Task instance with updated due_date if frequency is 'daily' or 'weekly',
            None if task is one-time (non-recurring).
        
        Example:
            scheduler.complete_task(daily_walk)  # Mark done
            new_instance = scheduler.reschedule_task(daily_walk)  # Auto-create for tomorrow
        """
        if task.frequency not in ["daily", "weekly"]:
            return None
        
        # Calculate next due date based on frequency
        today = datetime.now().date()
        if task.frequency == "daily":
            next_due_date = today + timedelta(days=1)
        elif task.frequency == "weekly":
            next_due_date = today + timedelta(days=7)
        else:
            return None
        
        # Create new task instance with same properties
        new_task = Task(
            description=task.description,
            duration=task.duration,
            frequency=task.frequency,
            time=task.time,
            due_date=next_due_date,
            completed=False,
            priority=task.priority
        )
        
        # Add the new task to the pet that owns the original task
        for pet in self.owner.get_all_pets():
            if task in pet.get_tasks():
                pet.add_care_need(new_task)
                break
        
        return new_task

    def detect_time_conflicts(self, tasks: Optional[List[Task]] = None) -> List[str]:
        """Identify scheduling conflicts where multiple tasks share the same time slot.
        
        Lightweight, non-blocking conflict detection that groups tasks by scheduled time.
        Checks for exact time-slot collisions (e.g., 09:00) and generates human-readable
        warnings. Tasks without scheduled times are ignored. Returns empty list if no conflicts.
        
        Note: This is exact-match detection; overlapping durations are not considered.
        For example, a task at 09:00 and another at 09:05 are not flagged as overlapping.
        
        Args:
            tasks: List of tasks to check. If None, checks all tasks owned by the owner.
        
        Returns:
            List of warning message strings. Empty if no conflicts detected.
        
        Example:
            conflicts = scheduler.detect_time_conflicts()
            if conflicts:
                for warning in conflicts:
                    print(warning)  # ⚠️  CONFLICT at 09:00: 3 tasks scheduled simultaneously
        """
        if tasks is None:
            tasks = self.retrieve_all_tasks()
        
        warnings: List[str] = []
        tasks_with_time = [t for t in tasks if t.time]  # Only check tasks with scheduled times
        
        # Build a dictionary of time -> list of tasks at that time
        time_map: Dict[str, List[Task]] = {}
        for task in tasks_with_time:
            if task.time not in time_map:
                time_map[task.time] = []
            time_map[task.time].append(task)
        
        # Generate warnings for any time slot with multiple tasks
        for time_slot, tasks_at_time in time_map.items():
            if len(tasks_at_time) > 1:
                task_descriptions = [f"'{t.description}'" for t in tasks_at_time]
                pet_info = []
                for task in tasks_at_time:
                    for pet in self.owner.get_all_pets():
                        if task in pet.get_tasks():
                            pet_info.append(f"{task.description} ({pet.name})")
                            break
                
                warning = f"⚠️  CONFLICT at {time_slot}: {len(tasks_at_time)} tasks scheduled simultaneously: {', '.join(task_descriptions)}"
                warnings.append(warning)
        
        return warnings
