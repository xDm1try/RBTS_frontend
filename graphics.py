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

        try:
            value = float(value)
            if value.is_integer():
                value = int(value)
        except ValueError:
            pass
        data[key] = value
    return data


def main():
    st.title("Просмотр данных из файла")

    uploaded_file = st.file_uploader("Выберите файл", type=["txt"])

    if uploaded_file is not None:

        try:
            lines = uploaded_file.readlines()

            lines = [line.decode('utf-8').strip() for line in lines]

            if lines:

                parsed_data = [parse_data_line(line) for line in lines]

                df = pd.DataFrame(parsed_data)

                if 'time' not in df.columns:
                    st.error("Файл должен содержать столбец 'time'.")
                    return
                else:
                    df['time'] = df['time'] - df['time'].iloc[0]

                current_columns = [col for col in df.columns if 'current' in col]
                voltage_columns = [col for col in df.columns if 'voltage' in col]
                temp_columns = [col for col in df.columns if 'temp' in col]
                other_numeric_columns = [
                    col for col in df.select_dtypes(include=['number']).columns
                    if col not in current_columns and col not in voltage_columns and col not in temp_columns and col != 'time'
                ]

                def create_plot(df, x_col, y_cols, title, x_title, y_title, show_legend=True):
                    fig = go.Figure()
                    colors = ['blue', 'green', 'orange', 'purple', 'red', 'cyan', 'magenta']
                    for idx, col in enumerate(y_cols):
                        fig.add_trace(go.Scatter(
                            x=df[x_col], 
                            y=df[col], 
                            mode='lines',
                            name=col,
                            line=dict(color=colors[idx % len(colors)], width=2.5)  # Увеличенная толщина линии
                        ))
                    fig.update_layout(
                        title=title,
                        xaxis_title=x_title,
                        yaxis_title=y_title,
                        template="plotly",
                        showlegend=show_legend,
                        margin=dict(l=50, r=50, t=50, b=50),
                        plot_bgcolor='white',
                        xaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',
                            linewidth=2,
                            mirror=True,
                            tickfont=dict(size=16, weight='bold')  # Жирные и крупные метки
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',
                            linewidth=2,
                            mirror=True,
                            tickfont=dict(size=16, weight='bold')  # Жирные и крупные метки
                        )
                    )
                    return fig

                if current_columns:
                    st.subheader("График токов")
                    fig_currents = create_plot(
                        df, 'time', current_columns, "График токов", "Время (сек)", "Значение"
                    )
                    st.plotly_chart(fig_currents, use_container_width=True)

                if voltage_columns:
                    st.subheader("График напряжений")
                    fig_voltages = create_plot(
                        df, 'time', voltage_columns, "График напряжений", "Время (сек)", "Значение"
                    )
                    st.plotly_chart(fig_voltages, use_container_width=True)

                if temp_columns:
                    st.subheader("График температур")
                    fig_temps = create_plot(
                        df, 'time', temp_columns, "График температур", "Время (сек)", "Значение"
                    )
                    st.plotly_chart(fig_temps, use_container_width=True)

                if current_columns and voltage_columns:
                    st.subheader("График напряжений и токов (две оси)")
                    fig_combined = go.Figure()

                    colors_voltage = ['blue', 'navy']
                    colors_current = ['red', 'darkred']

                    for idx, col in enumerate(voltage_columns):
                        fig_combined.add_trace(go.Scatter(
                            x=df['time'], 
                            y=df[col],
                            mode='lines', 
                            name=f"Напряжение: {col}", 
                            yaxis="y1",
                            line=dict(color=colors_voltage[idx % len(colors_voltage)], width=2.5)
                        ))

                    for idx, col in enumerate(current_columns):
                        fig_combined.add_trace(go.Scatter(
                            x=df['time'], 
                            y=df[col],
                            mode='lines', 
                            name=f"Ток: {col}", 
                            yaxis="y2",
                            line=dict(color=colors_current[idx % len(colors_current)], width=2.5)
                        ))

                    fig_combined.update_layout(
                        title="График напряжений и токов",
                        xaxis_title="Время (сек)",
                        yaxis=dict(
                            title="Напряжение mV",
                            side="left",
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',
                            linewidth=2,
                            mirror=True,
                            tickfont=dict(size=16, weight='bold')
                        ),
                        yaxis2=dict(
                            title="Ток mA",
                            overlaying="y",
                            side="right",
                            showgrid=False,
                            linecolor='black',
                            linewidth=2,
                            mirror=True,
                            tickfont=dict(size=16, weight='bold')
                        ),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        template="plotly",
                        margin=dict(l=50, r=50, t=50, b=50),
                        plot_bgcolor='white',
                        xaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            linecolor='black',
                            linewidth=2,
                            mirror=True,
                            tickfont=dict(size=16, weight='bold')
                        )
                    )
                    st.plotly_chart(fig_combined, use_container_width=True)

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