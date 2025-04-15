import streamlit as st
import requests

# Базовый URL вашего API
API_URL = "http://localhost:21216/batteries/"

# Функция для получения списка аккумуляторов
def fetch_batteries():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Ошибка при получении данных аккумуляторов")
        return []

# Функция для получения данных одного аккумулятора
def fetch_battery(battery_id):
    response = requests.get(f"{API_URL}{battery_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Аккумулятор не найден")
        return None

# Функция для создания нового аккумулятора
def create_battery(serial_number, capacity, comments):
    data = {
        "serial_number": serial_number,
        "capacity": capacity,
        "comments": comments
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        st.success("Аккумулятор успешно добавлен!")
    elif response.status_code == 400:
        st.error("Ошибка: Серийный номер уже зарегистрирован.")
    else:
        st.error("Ошибка при добавлении аккумулятора.")

# Функция для обновления данных аккумулятора
def update_battery(battery_id, serial_number, capacity, comments):
    data = {
        "serial_number": serial_number,
        "capacity": capacity,
        "comments": comments
    }
    response = requests.put(f"{API_URL}{battery_id}", json=data)
    if response.status_code == 200:
        st.success("Аккумулятор успешно обновлен!")
    else:
        st.error("Ошибка при обновлении аккумулятора")

# Функция для удаления аккумулятора
def delete_battery(battery_id):
    response = requests.delete(f"{API_URL}{battery_id}")
    if response.status_code == 200:
        st.success("Аккумулятор успешно удален!")
    else:
        st.error("Ошибка при удалении аккумулятора")

# Основная функция Streamlit
def main():
    st.title("Редактирование аккумуляторов")

    # Раздел для добавления нового аккумулятора
    st.subheader("Добавление нового аккумулятора")
    new_serial_number = st.text_input("Серийный номер")
    new_capacity = st.number_input("Емкость", min_value=1)
    new_comments = st.text_area("Комментарии")

    if st.button("Добавить аккумулятор"):
        if not new_serial_number:
            st.error("Серийный номер не может быть пустым.")
        elif new_capacity <= 0:
            st.error("Емкость должна быть больше 0.")
        else:
            create_battery(new_serial_number, new_capacity, new_comments)
            st.rerun()  # Обновляем страницу после добавления

    # Получение списка аккумуляторов
    batteries = fetch_batteries()

    if not batteries:
        st.warning("Список аккумуляторов пуст.")
        return

    # Выбор аккумулятора для редактирования
    battery_options = {battery["id"]: f"{battery['serial_number']} (ID: {battery['id']})" for battery in batteries}
    selected_battery_id = st.selectbox("Выберите аккумулятор для редактирования", list(battery_options.keys()), format_func=lambda x: battery_options[x])

    # Загрузка данных выбранного аккумулятора
    selected_battery = fetch_battery(selected_battery_id)
    if selected_battery:
        st.subheader("Текущие данные аккумулятора")
        st.write(f"ID: {selected_battery['id']}")
        st.write(f"Серийный номер: {selected_battery['serial_number']}")
        st.write(f"Емкость: {selected_battery['capacity']}")
        st.write(f"Комментарии: {selected_battery['comments']}")

        # Форма для редактирования
        st.subheader("Редактирование данных аккумулятора")
        updated_serial_number = st.text_input("Новый серийный номер", value=selected_battery['serial_number'])
        updated_capacity = st.number_input("Новая емкость", value=selected_battery['capacity'])
        updated_comments = st.text_area("Новые комментарии", value=selected_battery['comments'])

        if st.button("Обновить"):
            update_battery(selected_battery_id, updated_serial_number, updated_capacity, updated_comments)

        # Удаление аккумулятора
        st.subheader("Удаление аккумулятора")
        if st.button("Удалить аккумулятор"):
            delete_battery(selected_battery_id)
            st.rerun()  # Обновляем страницу после удаления

if __name__ == "__main__":
    main()