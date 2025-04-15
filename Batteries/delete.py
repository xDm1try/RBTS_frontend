import streamlit as st
import requests

from constants import API_URL


def get_batteries():
    response = requests.get(f"{API_URL}/batteries/")
    response.raise_for_status()
    return response.json()


def delete_battery(battery_id: int):
    response = requests.delete(f"{API_URL}/batteries/{battery_id}")
    response.raise_for_status()
    return response.json()


st.title("Удалить аккумулятор")

batteries = get_batteries()
if batteries:
    battery_options = {f"#{b['id']} - {b['serial_number']}": b['id'] for b in batteries}
    selected_battery = st.selectbox(
        "Выберите аккумулятор для удаления",
        options=list(battery_options.keys())
    )
    battery_id = battery_options[selected_battery]

    battery = next(b for b in batteries if b["id"] == battery_id)
    st.warning(f"Вы уверены, что хотите удалить аккумулятор #{battery['id']} - {battery['serial_number']}?")

    if st.button("Подтвердить удаление"):
        try:
            deleted_battery = delete_battery(battery_id)
            st.success(f"Аккумулятор #{deleted_battery['id']} успешно удален!")
            st.rerun()  # Обновляем список после удаления
        except requests.exceptions.HTTPError as e:
            st.error(f"Ошибка: {e.response.json().get('detail', 'Неизвестная ошибка')}")
else:
    st.info("Нет аккумуляторов для удаления")
