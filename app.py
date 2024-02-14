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


st.title('Forecasting the closing price of Mastercard assets')
with st.expander("Описание проекта"):
    st.write('''This project can be used to analyze market activity and trends for Mastercard, as well as for decision-making in investment strategy.''')


number_inputs_container = st.container(border=True)


number_inputs_container.number_input("Day's Open", key='open_price')
number_inputs_container.write(st.session_state.open_price)

number_inputs_container.number_input('Intraday High', key='high')
number_inputs_container.write(st.session_state.high)

number_inputs_container.number_input('Intraday Low', key='low')
number_inputs_container.write(st.session_state.low)

number_inputs_container.number_input('Volume', key='volume')
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


st.button("Reset", type="primary", on_click=reload)
if st.button('Predict'):    
    message = st.chat_message("assistant")
    message.write("The approximate price of the asset at the end of the trading day is:")
    message.write(round(predict_close(), 2))
else:  
    message = st.chat_message("assistant")   
    message.write("Awaiting data for forecasting...")
    message.write("Zzzzzzz...")