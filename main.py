import streamlit as st

devices = st.Page(
    "Devices/devices.py", title="Devices", icon="🤖", 
)

local_file = st.Page(
    "graphics.py", title="Parse file", icon="📂", 
)

bat_view = st.Page(
    "Batteries/view.py", title="View", icon="📜", 
)
bat_edit = st.Page(
    "Batteries/edit.py", title="Edit", icon="📝", 
)
bat_delete = st.Page(
    "Batteries/delete.py", title="Delete", icon="🪫", 
)
bat_add = st.Page(
    "Batteries/add.py", title="Add", icon="🔋", 
)

pg = st.navigation(
    {
        "Devices": [devices],
        "Batteries": [bat_view, bat_add, bat_edit, bat_delete],
        "Tests": [local_file],
    }
)


pg.run()
