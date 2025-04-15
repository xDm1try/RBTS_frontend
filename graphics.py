import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def parse_data_line(line):
    """
    Парсит строку данных и возвращает словарь с ключами и значениями.
    """
    data = {}
    pairs = line.split()
    for pair in pairs:
        key, value = pair.split('=')
        # Попробуем преобразовать значение в число (float или int)
        try:
            value = float(value)
            if value.is_integer():
                value = int(value)  # Если значение целое, преобразуем в int
        except ValueError:
            pass  # Если не число, оставляем как строку
        data[key] = value
    return data

def main():
    st.title("Просмотр данных из файла")

    # Виджет для загрузки файла
    uploaded_file = st.file_uploader("Выберите файл", type=["txt"])

    if uploaded_file is not None:
        # Чтение данных из загруженного файла
        try:
            lines = uploaded_file.readlines()

            # Декодируем строки из байтов в текст
            lines = [line.decode('utf-8').strip() for line in lines]

            # Проверяем, что файл содержит данные
            if lines:
                # Парсим все строки
                parsed_data = [parse_data_line(line) for line in lines]

                # Создаем DataFrame из спарсенных данных
                df = pd.DataFrame(parsed_data)

                # Проверяем наличие столбца 'time'
                if 'time' not in df.columns:
                    st.error("Файл должен содержать столбец 'time'.")
                    return

                # Группировка данных по типу: current, voltage, temp
                current_columns = [col for col in df.columns if 'current' in col]
                voltage_columns = [col for col in df.columns if 'voltage' in col]
                temp_columns = [col for col in df.columns if 'temp' in col]
                other_numeric_columns = [
                    col for col in df.select_dtypes(include=['number']).columns
                    if col not in current_columns and col not in voltage_columns and col not in temp_columns and col != 'time'
                ]

                # Функция для создания графика с Plotly
                def create_plot(df, x_col, y_cols, title, x_title, y_title, show_legend=True):
                    fig = go.Figure()
                    for col in y_cols:
                        fig.add_trace(go.Scatter(x=df[x_col], y=df[col], mode='lines', name=col))
                    fig.update_layout(
                        title=title,
                        xaxis_title=x_title,
                        yaxis_title=y_title,
                        template="plotly",
                        showlegend=show_legend,
                        margin=dict(l=50, r=50, t=50, b=50),  # Отступы для границ
                        plot_bgcolor='white',  # Цвет фона графика
                        xaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',  # Цвет линии оси X
                            linewidth=2,        # Толщина линии оси X
                            mirror=True         # Зеркальное отражение оси X
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',  # Цвет линии оси Y
                            linewidth=2,        # Толщина линии оси Y
                            mirror=True         # Зеркальное отражение оси Y
                        )
                    )
                    return fig

                # График для токов
                if current_columns:
                    st.subheader("График токов")
                    fig_currents = create_plot(
                        df, 'time', current_columns, "График токов", "Время (сек)", "Значение"
                    )
                    st.plotly_chart(fig_currents, use_container_width=True)

                # График для напряжений
                if voltage_columns:
                    st.subheader("График напряжений")
                    fig_voltages = create_plot(
                        df, 'time', voltage_columns, "График напряжений", "Время (сек)", "Значение"
                    )
                    st.plotly_chart(fig_voltages, use_container_width=True)

                # График для температур
                if temp_columns:
                    st.subheader("График температур")
                    fig_temps = create_plot(
                        df, 'time', temp_columns, "График температур", "Время (сек)", "Значение"
                    )
                    st.plotly_chart(fig_temps, use_container_width=True)

                # График с двумя осями для напряжений и токов
                if current_columns and voltage_columns:
                    st.subheader("График напряжений и токов (две оси)")
                    fig_combined = go.Figure()

                    # Добавляем напряжения на первую ось Y
                    for col in voltage_columns:
                        fig_combined.add_trace(go.Scatter(x=df['time'], y=df[col], mode='lines', name=f"Напряжение: {col}", yaxis="y1"))

                    # Добавляем токи на вторую ось Y
                    for col in current_columns:
                        fig_combined.add_trace(go.Scatter(x=df['time'], y=df[col], mode='lines', name=f"Ток: {col}", yaxis="y2"))

                    # Настройка макета графика
                    fig_combined.update_layout(
                        title="График напряжений и токов",
                        xaxis_title="Время (сек)",
                        yaxis=dict(
                            title="Напряжение",
                            side="left",
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',  # Цвет линии оси Y
                            linewidth=2,        # Толщина линии оси Y
                            mirror=True         # Зеркальное отражение оси Y
                        ),
                        yaxis2=dict(
                            title="Ток",
                            overlaying="y",
                            side="right",
                            showgrid=False,
                            linecolor='black',  # Цвет линии второй оси Y
                            linewidth=2,        # Толщина линии второй оси Y
                            mirror=True         # Зеркальное отражение второй оси Y
                        ),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        template="plotly",
                        margin=dict(l=50, r=50, t=50, b=50),  # Отступы для границ
                        plot_bgcolor='white',  # Цвет фона графика
                        xaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',  # Цвет линии оси X
                            linewidth=2,        # Толщина линии оси X
                            mirror=True         # Зеркальное отражение оси X
                        )
                    )
                    st.plotly_chart(fig_combined, use_container_width=True)

                # Графики для остальных числовых параметров
                if other_numeric_columns:
                    st.subheader("Графики других параметров")
                    for column in other_numeric_columns:
                        fig_other = create_plot(
                            df, 'time', [column], f"График для параметра: {column}", "Время (сек)", "Значение"
                        )
                        st.plotly_chart(fig_other, use_container_width=True)

            else:
                st.warning("Файл пуст.")

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")

    else:
        st.info("Пожалуйста, загрузите файл.")

main()