import streamlit as st

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
        "Batteries": [bat_view, bat_add, bat_edit, bat_delete],
        "Tests": [local_file],
    }
)


pg.run()
