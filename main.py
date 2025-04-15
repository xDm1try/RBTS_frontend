import streamlit as st

# Настройка главной страницы
# Настройка страницы

st.title("Главная страница")

st.write("Добро пожаловать в систему тестирования аккумуляторами!")

# main = st.Page(
#     "main.py", title="Main", icon="🔋", 
# )
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
        "Tests": [],
    }
)


pg.run()
