from pawpal_system import Owner, Pet, Scheduler, Task
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

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
owner_name = st.text_input("Owner name", value=owner.name)

if st.button("Save owner"):
    owner.name = owner_name
    st.session_state.owner = owner
    st.success(f"Owner updated to {owner.name}.")

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted = st.form_submit_button("Add pet")

    if submitted:
        new_pet = Pet(name=pet_name, species=species)
        owner.add_pet(new_pet)
        st.session_state.owner = owner
        st.success(f"{pet_name} added to {owner.name}'s pets.")

st.markdown("### Current Pets")
if owner.get_pets():
    for pet in owner.get_pets():
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Schedule a Task")
if owner.get_pets():
    pet_names = [pet.name for pet in owner.get_pets()]
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = next(pet for pet in owner.get_pets() if pet.name == selected_pet_name)

    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        scheduled_time = st.text_input("Time", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        task_submitted = st.form_submit_button("Add task")

        if task_submitted:
            task = Task(description=task_title, scheduled_time=scheduled_time, frequency=frequency)
            selected_pet.add_task(task)
            st.session_state.owner = owner
            st.success(f"Task added for {selected_pet.name}.")
else:
    st.info("Add a pet first to schedule tasks.")

st.markdown("### Current Tasks")
if owner.get_all_tasks():
    task_rows = []
    for pet in owner.get_pets():
        for task in pet.get_tasks():
            task_rows.append(
                {
                    "pet": pet.name,
                    "task": task.description,
                    "time": task.scheduled_time,
                    "frequency": task.frequency,
                }
            )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button now uses the scheduler logic to organize tasks.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    ordered_tasks = scheduler.organize_tasks()
    pending_tasks = scheduler.get_pending_tasks()
    recurring_tasks = scheduler.handle_recurring_tasks()

    st.success("Schedule generated from your owner, pet, and task data.")

    if ordered_tasks:
        st.subheader("Sorted Tasks")
        rows = []
        for task in ordered_tasks:
            pet_name = next((pet.name for pet in owner.get_pets() if task in pet.get_tasks()), "Unknown")
            rows.append(
                {
                    "pet": pet_name,
                    "task": task.description,
                    "time": task.scheduled_time,
                    "frequency": task.frequency,
                    "completed": task.completed,
                }
            )
        st.table(rows)

    if recurring_tasks:
        st.caption(f"Recurring tasks included: {', '.join(task.description for task in recurring_tasks)}")

    if scheduler.has_conflicts():
        st.warning("Conflicting tasks detected: two or more tasks share the same time slot.")

    st.caption(f"{len(pending_tasks)} pending tasks remain.")
