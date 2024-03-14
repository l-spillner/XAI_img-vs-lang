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
        button[kind="headerNoPadding"] {display:none;}
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


############################################################ MAIN ############################################################


st.write('''__Impressum__

Universität Bremen  
Bibliothekstraße 1  
D-28359 Bremen  

__Rechtsform__

Die Universität Bremen ist eine Körperschaft des Öffentlichen Rechts. Sie wird durch die Rektorin Prof. Dr. Jutta Günther gesetzlich vertreten.
Zuständige Aufsichtsbehörde ist die Senatorin für Wissenschaft und Häfen, Katharinenstraße 37, 28195 Bremen.

__Inhaltliche Verantwortlichkeit i. S. v. § 5 TMG und § 18 Abs. 2 MStV__

Für die Richtigkeit und Aktualität der veröffentlichten Inhalte (auch Kommentare von Leser*innen) sind die jeweiligen Ersteller*innen der einzelnen Seiten verantwortlich. Trotz sorgfältiger inhaltlicher Kontrolle übernehmen wir keine Haftung für die Inhalte externer Links. Für den Inhalt der verlinkten Seiten sind ausschließlich deren Betreiber verantwortlich.

Rachel Ringe  
Universität Bremen  
Bibliothekstraße 5  
D-28359 Bremen  
Tel.: +49 421 218 64414  
E-Mail: rringe@uni-bremen.de  

__Technische Verantwortlichkeit i. S. v. § 5 TMG und § 18 Abs. 2 MStV__

Rachel Ringe  
Universität Bremen  
Bibliothekstraße 5  
D-28359 Bremen  
Tel.: +49 421 218 64414  
E-Mail: rringe@uni-bremen.de ''')

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



