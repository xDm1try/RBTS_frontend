import streamlit as st
import requests

from constants import API_URL


def get_batteries():
    response = requests.get(f"{API_URL}/batteries/")
    response.raise_for_status()
    return response.json()


def update_battery(battery_id: int, serial_number: str, capacity: int, comments: str):
    data = {
        "serial_number": serial_number,
        "capacity": capacity,
        "comments": comments if comments else None
    }
    response = requests.put(f"{API_URL}/batteries/{battery_id}", json=data)
    response.raise_for_status()
    return response.json()


st.title("Редактировать аккумулятор")

batteries = get_batteries()
if batteries:
    battery_options = {f"#{b['id']} - {b['serial_number']}": b['id'] for b in batteries}
    selected_battery = st.selectbox(
        "Выберите аккумулятор для редактирования",
        options=list(battery_options.keys())
    )
    battery_id = battery_options[selected_battery]

    battery = next(b for b in batteries if b["id"] == battery_id)
    with st.form("edit_battery"):
        new_serial_number = st.text_input("Серийный номер*", value=battery["serial_number"], max_chars=50)
        new_capacity = st.number_input("Ёмкость*", value=battery["capacity"], min_value=1, step=1)
        new_comments = st.text_area(
            "Комментарии", value=battery["comments"] if battery["comments"] else "", max_chars=200)

        if st.form_submit_button("Обновить"):
            if not new_serial_number or not new_capacity:
                st.error("Поля с * обязательны для заполнения")
            else:
                try:
                    updated_battery = update_battery(battery_id, new_serial_number, new_capacity, new_comments)
                    st.success(f"Аккумулятор #{updated_battery['id']} успешно обновлен!")
                except requests.exceptions.HTTPError as e:
                    st.error(f"Ошибка: {e.response.json().get('detail', 'Неизвестная ошибка')}")
else:
    st.info("Нет аккумуляторов для редактирования")
