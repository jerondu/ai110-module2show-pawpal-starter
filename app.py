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

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    today_schedule = scheduler.generate_schedule(date="today")

    if not today_schedule.tasks:
        st.info("No due tasks to schedule.")
    else:
        st.write("## Today's Schedule")
        for task in today_schedule.tasks:
            status = "Done" if task.completed else "Pending"
            st.write(f"- {task.description}, duration {task.duration} min, priority {task.priority}, status {status}")

    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
