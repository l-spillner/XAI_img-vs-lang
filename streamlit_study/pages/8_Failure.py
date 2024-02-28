############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from annotated_text import annotated_text
from streamlit_extras.switch_page_button import switch_page
import webbrowser
import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re
from collections import Counter

############################################################ Settings

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# hides button to close sidebar, open settings
no_button_style = """
    <style>
        button[kind="header"] {display:none;}
    </style>
"""
st.markdown(no_button_style, unsafe_allow_html=True)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

############################################################ Public variables

############################################################ Public functions

def redirect(_url):
	link = ''
	st.markdown(link, unsafe_allow_html=True)


############################################################ MAIN ############################################################

try:
	project_path = st.session_state.project_path
	df = st.session_state.data
	#conversion = st.session_state.conversion
	student_order = st.session_state.student_order
	AI_predictions = st.session_state.AI_predictions
	#df_full = st.session_state.data_full
	#data_path = os.path.join(st.session_state.project_path, "sample.csv")
	group = st.session_state.group
	filename = st.session_state.filename
	state_num = st.session_state.state_num
	student_num = st.session_state.student_num
	#indexes = st.session_state.indexes
	#explanations_num = st.session_state.x_num
	
except:
	st.session_state.reroute_error = True
	switch_page("Home")

st.write("# Please return your submission")
st.write("Unfortunately you did not answer the comprehension test questions correctly and will thus not be able to participate in our study. Please go back to Prolific and return your submission.")

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
</style>
<p><a href="https://hai.uni-bremen.de/Imprint" target="_blank">Imprint</a> | <a href="https://www.uni-bremen.de/en/data-privacy" target="_blank">Privacy Policy</a></p>
"""
st.write(footer,unsafe_allow_html=True)


