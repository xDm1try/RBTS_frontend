import streamlit as st
import requests

from constants import API_URL


def create_battery(serial_number: str, capacity: int, comments: str):
    data = {
        "serial_number": serial_number,
        "capacity": capacity,
        "comments": comments if comments else None
    }
    response = requests.post(f"{API_URL}/batteries/", json=data)
    response.raise_for_status()
    return response.json()


st.title("Добавить новый аккумулятор")

with st.form("add_battery"):
    serial_number = st.text_input("Серийный номер*", max_chars=50)
    capacity = st.number_input("Ёмкость*", min_value=1, step=1)
    comments = st.text_area("Комментарии", max_chars=200)

    if st.form_submit_button("Сохранить"):
        if not serial_number or not capacity:
            st.error("Поля с * обязательны для заполнения")
        else:
            try:
                created_battery = create_battery(serial_number, capacity, comments)
                st.success(f"Аккумулятор #{created_battery['id']} успешно добавлен!")
            except requests.exceptions.HTTPError as e:
                st.error(f"Ошибка: {e.response.json().get('detail', 'Неизвестная ошибка')}")
