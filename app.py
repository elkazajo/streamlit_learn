import streamlit as st
import pandas as pd
import numpy as np
import pickle   


can_reload = False


st.title('Прогнозирование цены активов Mastercard')
with st.expander("Описание проекта"):
    st.write('''Данный проект может использоваться для анализа рыночной активности и трендов по Mastercard, а также для принятия решений в инвестиционной стратегии.''')


number_inputs_container = st.container(border=True)


open_price = number_inputs_container.number_input('Цена актива в начале торгового дня')
number_inputs_container.write(open_price)

high = number_inputs_container.number_input('Максимальная цена актива за торговый день')
number_inputs_container.write(high)

low = number_inputs_container.number_input('Минимальная цена актива за торговый день')
number_inputs_container.write(low)

volume = number_inputs_container.number_input('Объем активов, проданных или купленных в течение торгового дня')
number_inputs_container.write(volume)

dividends = number_inputs_container.number_input('Дивиденды, выплаченные в этот день (0 если не было)')
number_inputs_container.write(dividends)


model_file_path = "models\project_1_mastercard.sav"
model = pickle.load(open(model_file_path, 'rb'))


@st.cache_data
def predict_close(open_price, high, low, volume, dividends):  
    input_dataframe = pd.DataFrame({
        'open' : open_price,
        'high' : high,
        'low' : low,
        'volume' : volume,
        'dividends' : dividends
    }, index=[0])

    input_data = np.log1p(input_dataframe)

    prediction = model.predict(input_data)

    return str(*np.expm1(prediction))


@st.cache_data
def reload():
    open_price = high = low = volume = dividends = 0.0
    return open_price, high, low, volume, dividends


st.button("Сбросить", type="primary")
if st.button('Предсказать'):    
    message = st.chat_message("assistant")
    message.write("Примерная цена актива в конце торгового дня:")
    message.write(predict_close(open_price, high, low, volume, dividends))
else:  
    open_price, high, low, volume, dividends = reload()
    message = st.chat_message("assistant")   
    message.write("Ожидаю данные для прогнозирования...")
    message.write("Бип боп биип...")