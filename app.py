import streamlit as st
import pandas as pd
import numpy as np
import pickle   


dividends = 0


if 'open_price' not in st.session_state:
    st.session_state.open_price = 0
if 'high' not in st.session_state:
    st.session_state.high = 0
if 'low' not in st.session_state:
    st.session_state.low = 0
if 'volume' not in st.session_state:
    st.session_state.volume = 0


st.title('Прогнозирование цены активов Mastercard')
with st.expander("Описание проекта"):
    st.write('''Данный проект может использоваться для анализа рыночной активности и трендов по Mastercard, а также для принятия решений в инвестиционной стратегии.''')


number_inputs_container = st.container(border=True)


number_inputs_container.number_input('Цена актива в начале торгового дня', key='open_price')
number_inputs_container.write(st.session_state.open_price)

number_inputs_container.number_input('Максимальная цена актива за торговый день', key='high')
number_inputs_container.write(st.session_state.high)

number_inputs_container.number_input('Минимальная цена актива за торговый день', key='low')
number_inputs_container.write(st.session_state.low)

number_inputs_container.number_input('Объем активов, проданных или купленных в течение торгового дня', key='volume')
number_inputs_container.write(st.session_state.volume)


model_file_path = "models\project_1_mastercard.sav"
model = pickle.load(open(model_file_path, 'rb'))


def predict_close():  
    input_dataframe = pd.DataFrame({
        'open' : st.session_state.open_price,
        'high' : st.session_state.high,
        'low' : st.session_state.low,
        'volume' : st.session_state.volume,
        'dividends' : dividends
    }, index=[0])

    input_data = np.log1p(input_dataframe)

    prediction = model.predict(input_data)

    return str(*np.expm1(prediction))


def reload():
    del st.session_state.open_price
    del st.session_state.high
    del st.session_state.low
    del st.session_state.volume


st.button("Сбросить", type="primary", on_click=reload)
if st.button('Предсказать'):    
    message = st.chat_message("assistant")
    message.write("Примерная цена актива в конце торгового дня:")
    message.write(predict_close())
else:  
    message = st.chat_message("assistant")   
    message.write("Ожидаю данные для прогнозирования...")
    message.write("Бип боп биип...")