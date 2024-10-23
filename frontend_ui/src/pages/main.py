import os
import json
import requests

import streamlit as st

host_name = os.getenv('FE_HOST_NAME')
be_port = os.getenv('BE_PORT')


st.title("Basic calculator app")

# taking user input
option = st.selectbox('What operation would you like to perform?', 
                      options=('Addition', 'Subtraction', 'Multiplication', 'Division'))

st.write("")
st.write("Select the numbers from slider bellow:")
# x = st.slider(label="X", min_value=0, max_value=100, value=20)
# y = st.slider(label="Y", min_value=0, max_value=130, value=10)

text = st.text_input("Completion prompt", value="Type here", max_chars=None)

# converting inputs into json format
inputs = {"query": text}



# When user clicks on button it will fetch the API
if st.button(label='Calculate'):
    res=requests.post(url=f"http://{host_name}:{be_port}/calculate", data=json.dumps(inputs))
    st.subheader(f"Reponse from API: {res.text}")