from pawpal_system import Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Owner vault check: reuse existing Owner object if present
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, email=f"{owner_name.lower()}@example.com", preferences={"work_hours": "9-17"})
else:
    existing_owner = st.session_state.owner
    if existing_owner.name != owner_name:
        existing_owner.name = owner_name
        existing_owner.email = f"{owner_name.lower()}@example.com"

# Pet add panel
st.markdown("### Add Pet")
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)
if st.button("Add pet"):
    new_pet = Pet(name=pet_name, type=species, age=pet_age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet {new_pet.name} ({new_pet.type})")

pets = st.session_state.owner.get_all_pets()
pet_options = [pet.name for pet in pets] if pets else []
selected_pet_name = st.selectbox("Select pet", options=pet_options or ["None"], index=0 if pet_options else 0)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_choice = st.selectbox("Priority", ["low", "medium", "high"], index=2)

priority_map = {"low": 1, "medium": 2, "high": 3}
if st.button("Add task"):
    if not pet_options:
        st.error("Add a pet first before adding tasks.")
    else:
        task = Task(description=task_title, duration=int(duration), frequency="daily", priority=priority_map[priority_choice])
        target_pet = next((p for p in pets if p.name == selected_pet_name), None)
        if target_pet:
            target_pet.add_care_need(task)
            st.success(f"Added task '{task_title}' to {target_pet.name}")
        else:
            st.error("Selected pet not found.")

# Check if there are any tasks across all pets
total_tasks = sum(len(pet.get_tasks()) for pet in pets)
if total_tasks > 0:
    st.success(f"✅ {total_tasks} task(s) added across your pets!")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate your daily schedule with intelligent sorting and conflict detection.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    today_schedule = scheduler.generate_schedule(date="today")

    if not today_schedule.tasks:
        st.info("No due tasks to schedule today.")
    else:
        # Sort tasks by time for better display
        sorted_tasks = scheduler.sort_by_time(today_schedule.tasks)
        
        # Check for conflicts
        conflicts = scheduler.detect_time_conflicts(today_schedule.tasks)
        
        if conflicts:
            st.warning("⚠️ **Scheduling Conflicts Detected!**")
            st.markdown("**These tasks are scheduled at the same time. Consider rescheduling to avoid overlap:**")
            for conflict in conflicts:
                st.error(f"• {conflict}")
            st.markdown("💡 **Tip:** Use the task editing features to adjust times and regenerate the schedule.")
            st.divider()
        
        st.success(f"✅ **Today's Schedule Generated** ({len(sorted_tasks)} tasks)")
        
        # Display tasks in a professional table
        task_data = []
        for task in sorted_tasks:
            status = "✅ Done" if task.completed else "⏳ Pending"
            time_display = task.time if task.time else "No time set"
            task_data.append({
                "Task": task.description,
                "Time": time_display,
                "Duration": f"{task.duration} min",
                "Priority": task.priority,
                "Status": status
            })
        
        st.table(task_data)
        
        # Summary stats
        pending_count = sum(1 for t in sorted_tasks if not t.completed)
        completed_count = len(sorted_tasks) - pending_count
        st.info(f"📊 **Summary:** {pending_count} pending tasks, {completed_count} completed tasks")

    st.markdown(
        """
**Scheduler Features Used:**
- Priority-based initial scheduling
- Time-based sorting for chronological display
- Conflict detection with helpful warnings
- Professional table layout for easy reading
"""
    )
