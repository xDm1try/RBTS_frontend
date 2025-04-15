import streamlit as st
from typing import List
import requests
from constants import API_URL


def get_batteries(skip: int = 0, limit: int = 100) -> List[dict]:
    response = requests.get(f"{API_URL}/batteries/?skip={skip}&limit={limit}")
    response.raise_for_status()
    return response.json()


st.title("Просмотр всех аккумуляторов")

batteries = get_batteries()
if batteries:
    for battery in batteries:
        with st.expander(f"Аккумулятор #{battery['id']} - {battery['serial_number']}"):
            st.write(f"**Серийный номер:** {battery['serial_number']}")
            st.write(f"**Ёмкость:** {battery['capacity']}")
            st.write(f"**Комментарии:** {battery['comments']}")
else:
    st.info("Аккумуляторы не найдены")
