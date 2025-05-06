import streamlit as st
import requests
from pydantic import BaseModel
from typing import List, Dict, Any


class DeviceAnnounce(BaseModel):
    device_status: str
    device_name: str
    device_ip: str
    sd_free_mem: int


def get_device_list():
    try:
        response = requests.get("http://localhost:21216/get_device_list")
        response.raise_for_status()
        devices = response.json()
        return [DeviceAnnounce(**device) for device in devices]
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при получении списка устройств: {e}")
        return []


def execute_device_action(params: Dict[str, Any]):
    params["sd_file"] = str(params["sd_file"])
    params["polling_rate"] = params["polling_rate"]

    st.json({"параметры": params})
    response = requests.post("http://localhost:21216/start_device_actions", json=params)
    st.success(f"Code {response.status_code=}")


st.set_page_config(page_title="Управление устройствами", layout="wide")

if 'selected_device' not in st.session_state:
    st.session_state.selected_device = None

if 'test_params' not in st.session_state:
    st.session_state.test_params = {
        "actions": [],
        "device_name": "",
        "device_ip": "",
        "sd_file": False,
        "filename": "discharge_log",
        "polling_rate": 5
    }

if st.session_state.selected_device:
    device = st.session_state.selected_device

    st.title(f"Управление устройством: {device.device_name}")
    st.write(f"**IP-адрес:** {device.device_ip}")
    st.write(f"**Статус:** {device.device_status}")
    st.write(f"**Свободная память:** {device.sd_free_mem} GB")

    st.session_state.test_params["device_name"] = device.device_name
    st.session_state.test_params["device_ip"] = device.device_ip

    st.markdown("---")
    st.subheader("Доступные действия")

    action_type = st.selectbox(
        "Добавить действие",
        ["", "Charge", "Discharge", "Wait"],
        key="action_type"
    )

    action_params = {}
    if action_type == "Wait":
        action_params["duration"] = str(st.number_input(
            "Длительность (сек)",
            min_value=1, max_value=100000, value=30, step=1,
            key="charge_duration"
        ))

    if action_type == "Charge":
        col1, col2 = st.columns(2)
        with col1:
            action_params["const_volt_mV"] = str(st.number_input(
                "Напряжение (mV)",
                min_value=3840, max_value=4608, value=4208, step=16,
                key="charge_voltage"
            ))
        with col2:
            action_params["const_current_mA"] = str(st.number_input(
                "Постоянный ток зарядки (mA)",
                min_value=64, max_value=5056, value=128, step=64,
                key="charge_current"
            ))
        col1, col2 = st.columns(2)
        with col1:
            action_params["cut_off_current_mA"] = str(st.number_input(
                "Предел тока для прекращения зарядки",
                min_value=2, max_value=int(action_params["const_current_mA"]),
                value=int(action_params["const_current_mA"]) // 2, step=1,
                key="cut_off_current"
            ))
        with col2:
            action_params["temp_bat_limit"] = str(st.number_input(
                "Максимальная температура (°C)",
                min_value=20, max_value=100, value=45, step=1,
                key="temp_bat_limit"
            ))
        action_params["timeout"] = st.checkbox(
            "Timeout действия",
            value=True,
            key="timeout"
        )
        if action_params["timeout"]:
            action_params["duration"] = str(st.number_input(
                "Длительность (сек)",
                min_value=1, max_value=100000, value=30, step=1,
                key="charge_duration"
            ))

    elif action_type == "Discharge":
        col1, col2 = st.columns(2)
        with col1:
            action_params["discharge_current"] = str(st.number_input(
                "Постояный ток разрядки (А)",
                min_value=5, max_value=1500, value=300, step=1,
                key="discharge_current"
            ))
            action_params["start_duty"] = str(st.number_input(
                "Стартовое значиение ШИМ",
                min_value=0, max_value=100, value=20, step=1,
                key="start_duty"
            ))
        with col2:
            action_params["dicharge_voltage_limit"] = str(st.number_input(
                "Порог напряжения для прекращения разрядки (В)",
                min_value=0, max_value=5000, value=2750, step=1,
                key="dicharge_voltage_limit"
            ))

        action_params["temp_bat_limit"] = str(st.number_input(
            "Максимальная температура (°C)",
            min_value=0, max_value=100, value=45, step=1,
            key="temp_bat_limit"
        ))
        action_params["timeout"] = st.checkbox(
            "Timeout действия",
            value=True,
            key="timeout"
        )
        if action_params["timeout"]:
            action_params["duration"] = str(st.number_input(
                "Длительность (сек)",
                min_value=1, max_value=100000, value=30, step=1,
                key="charge_duration"
            ))

    if action_type and st.button("Добавить действие в очередь"):
        new_action = {
            "type": action_type,
            "params": action_params,
        }
        st.session_state.test_params["actions"].append(new_action)
        st.success(f"Действие '{action_type}' добавлено в очередь!")

    if st.session_state.test_params["actions"]:
        st.markdown("---")
        st.subheader("Очередь действий")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.session_state.test_params["sd_file"] = st.checkbox(
                "Запись на SD card",
                value=True,
                key="sd_file_checkbox"
            )
        if st.session_state.test_params["sd_file"]:
            with col2:
                st.session_state.test_params["filename"] = st.text_input(
                    "Название файла",
                    value="discharge_log",
                    key="filename_input"
                )
            with col3:
                st.session_state.test_params["polling_rate"] = str(st.number_input(
                    "Частота опроса (сек)",
                    min_value=1,
                    max_value=60,
                    value=5,
                    key="polling_rate_input"
                )
                )
        # st.session_state.test_params["sd_file"] = str(st.session_state.test_params["sd_file"])

        st.write(f"Устройство: {st.session_state.test_params['device_ip']}")

        for i, action in enumerate(st.session_state.test_params["actions"], 1):
            with st.expander(f"Действие #{i}: {action['type']}"):
                st.write("Параметры:")
                st.json(action["params"])

                if st.button(f"Удалить действие #{i}", key=f"remove_{i}"):
                    st.session_state.test_params["actions"].pop(i-1)
                    st.rerun()

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Запустить все действия", type="primary"):
                import pprint as pp
                pp.pprint(st.session_state.test_params)
                execute_device_action(st.session_state.test_params)
                st.session_state.test_params["actions"] = []
        with col2:
            if st.button("Очистить очередь"):
                st.session_state.test_params["actions"] = []
                st.rerun()
        with col3:
            if st.button("Вернуться к списку устройств"):
                st.session_state.selected_device = None
                st.rerun()
    else:
        st.markdown("---")
        if st.button("Вернуться к списку устройств"):
            st.session_state.selected_device = None
            st.rerun()

else:
    st.title("Список доступных устройств")

    if st.button("Обновить список устройств"):
        st.rerun()

    devices = get_device_list()

    if devices:
        st.write("### Список устройств")
        cols = st.columns([1, 2, 2, 2, 2])
        with cols[0]:
            st.write("**Статус**")
        with cols[1]:
            st.write("**Имя устройства**")
        with cols[2]:
            st.write("**IP-адрес**")
        with cols[3]:
            st.write("**Свободная память (SD)**")
        with cols[4]:
            st.write("**Действия**")

        for device in devices:
            cols = st.columns([1, 2, 2, 2, 2])
            with cols[0]:
                status_color = "green" if device.device_status.lower() == "online" else "red"
                st.markdown(f"<span style='color:{status_color}'>{device.device_status}</span>", unsafe_allow_html=True)
            with cols[1]:
                st.write(device.device_name)
            with cols[2]:
                st.write(device.device_ip)
            with cols[3]:
                st.write(f"{device.sd_free_mem} MB")
            with cols[4]:
                if st.button("Управление", key=f"manage_{device.device_ip}"):
                    st.session_state.selected_device = device
                    st.rerun()
    else:
        st.warning("Устройства не найдены или произошла ошибка при получении данных.")
