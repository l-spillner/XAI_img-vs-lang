############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re

############################################################ Settings

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# hides the first option in a radio group
# note: this applies to ALL radio groups across the app; it cannot be done for an individual button!
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

no_sidebar_style = """
	<style>
        div[data-testid="stSidebarNav"] {pointer-events: none; cursor: default;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# hides button to close sidebar, open settings
no_button_style = """
    <style>
        button[kind="headerNoPadding"] {display:none;}
    </style>
"""
st.markdown(no_button_style, unsafe_allow_html=True)

############################################################ Public variables

# paths & data
project_path = os.path.dirname(os.path.dirname(__file__))
dataset_path = os.path.join(project_path, 'data/dataset_converted.csv')
#datavalues_path = os.path.join(project_path, 'data/dataset_values.txt')
dataxai_path = os.path.join(project_path, 'data/explanations_lang.json')

st.session_state.project_path = project_path

user_predictions = {}
st.session_state.user_predictions = user_predictions
student_num = 0
st.session_state.student_num = student_num
st.session_state.state_num = 1

st.session_state.attention_num = 0

# read data

# dataset (without target value)
df = pd.read_csv(dataset_path, index_col = 0)
df = df.drop(["Target"], axis = 1)
df = df.round({'Avg. grade (1st semester)': 3})
df = df.astype({'Avg. grade (1st semester)': 'str'}, errors='ignore') # if I don't do this, grades will still be converted to int 
	# when the dataframe is transposed to one-student-table later...
	# but it's enough to do it only for the first semester grade and then it works also for the second semester grade.
	# I have no idea what's going on.

# subset with predictions and explanations
with open(dataxai_path) as file:
    AI_predictions = json.load(file)
st.session_state.AI_predictions = AI_predictions

# tutorial student

student_id_tutorial = 2309 	# all courses examined and passed
							# good grades
							# male
st.session_state.comprehension = True

# randomly select ten of the students 

students = list(AI_predictions.keys())
students = [int(s) for s in students if not int(s) == student_id_tutorial]
students_plus_tutorial = students+[student_id_tutorial]
df = df.loc[students_plus_tutorial]
student_order = random.sample(students, 10)
random.shuffle(student_order)
student_order = student_order[:6] + [student_id_tutorial] + student_order[6:]
#st.write(student_order)
#df["Order"] = student_order
#df.set_index('Order',inplace=True)
st.session_state.data = df
st.session_state.student_order = student_order
st.session_state.student_id_tutorial = student_id_tutorial
st.session_state.tutorial_done = False

#df["ai_prop"] = [AI_predictions[str(s)]['grad_prob'] for s in df.index]
#st.write(df)

# # Randomly shuffle data
# df = pd.read_csv(data_path, index_col = 0)
# df_random = df.sample(frac=1)
# # Save data including target
# st.session_state.data_full = df
# # Adjust version of data for display
# df_display = df.loc[:, ~df.columns.isin(['Target', 'AI prediction', 'explanation_num', 'explanation_cat'])]
# randomized_indexes = df_random.index.tolist()
# st.session_state.indexes = randomized_indexes
# for i in range(15):
# 	df_display.at[randomized_indexes[i],"DisplayIndex"] = "Student " + str(i + 1)
# df_display.set_index('DisplayIndex',inplace=True)
# st.session_state.data = df_display

# explanations_num = {'Age at enrollment': 'low',
#  'Curricular units 1st sem enrolled': 'high',
#  'Curricular units 1st sem grade': 'high',
#  'Curricular units 1st sem passed': 'high',
#  'Curricular units 1st sem recognized from previous education or work': 'na',
#  'Curricular units 1st sem without exams': 'na',
#  'Curricular units 2nd sem enrolled': 'high',
#  'Curricular units 2nd sem grade': 'high',
#  'Curricular units 2nd sem passed': 'high',
#  'Curricular units 2nd sem recognized from previous education or work': 'na',
#  'Curricular units 2nd sem without exams': 'na',
#  'GDP at enrollment': 'na',
#  'Inflation rate at enrollment': 'na',
#  'Total exams across all classes in 1st sem': 'low',
#  'Total exams across all classes in 2nd sem': 'low',
#  'Unemployment rate at enrollment': 'na',
#  "University's position in preferences when applying": 'high'}
# st.session_state.x_num = explanations_num

############################################################ sort user into group

# group 0 gets visual explanations
# group 1 gets lang explanations

if not "group" in st.session_state:

	dirs = os.listdir('study_data')
	dirs = [(d.startswith('1_')) for d in dirs]

	# zeroCounter = 0
	# while os.path.exists('study_data/0_' + str(zeroCounter)+'.csv'):
	# 	zeroCounter = zeroCounter + 1
	# oneCounter = 0
	# while os.path.exists('study_data/1_' + str(oneCounter)+'.csv'):
	# 	oneCounter = oneCounter + 1

	# st.write(zeroCounter, oneCounter)

	if sum(dirs) >= (len(dirs)-sum(dirs)): # sum is num group 1, len is num all, len-sum is num group 0
		st.session_state.group = 0	
	else:
		st.session_state.group = 1



############################################################ Public functions




############################################################ MAIN ############################################################

if "reroute_error" in st.session_state and st.session_state.reroute_error:
	st.warning("Sorry! The page was reloaded in your browser, which started a new session. As this site does not save any cookies, it's not possible to remember data between sessions. Please start again.")

############################################################ load data


# show of hide data for debug
if False:

	st.write("This is the data:")
	st.write(df)

	st.write("But participants won't actually see this; it's just for us to check. Instead, they only see the lower part:")
	st.write("---")

############################################################ text

st.write("# Academic Career Predictions")

st.markdown(
f"""
This is a research study on the usefulness of Artificial Intelligence (AI) decision aids to predict the outcome of a student's academic career.

Students dropping out before finishing their degree impacts economic growth, employment, competiveness as well as students' lives and families as well as educational institutions. Tutors and advisors can use student data to make predictions about their academic career to offer more accurate help to students.

Your task will be to have a look at 12 randomly selected sets of student data, and predict if the student will graduate or drop out.
Our AI tool trained specifically for this task will make a recommendation to assist you with your decision. Finally, we will ask you to answer a few questions about how useful the AI tool was in making your decisions.""")



st.markdown(
f"""
---
##### About this study:

The entire study should take about 20 minutes. All your answers will be collected anonymously. We do not collect personal information, like your name or IP address. You are free to quit the study at any time.

The data that we collect is stored on a server of the University of Bremen, in Germany. After the study finishes, the data from all participants will be analysed together and the results might be published in future research papers. After finishing the experiment, it is not possible to withdraw your data because of the anonymization. 

If you have any questions about this study, please contact:

Laura Spillner (laura.spillner@uni-bremen.de) or Rachel Ringe (rringe@uni-bremen.de)

If you want to proceed with the study, please click "Start"!

"""
)

q1 = st.text_input('Please enter your Prolific Id:')

next_page = st.button("Start", key = 1)
if next_page:
	
	if(q1 == ""):
		st.error("Please enter your Prolific ID to start")
	else:
		#id = 0
		#while os.path.exists(str(st.session_state.group) + '_' + str(id)+'.csv'):
		#	id = id + 1
		filename = 'study_data/' + str(st.session_state.group) + '_' + q1 + '.csv'
		st.session_state.filename = filename
		with open(filename, 'a+') as f:
			f.write(f"Prolific ID,{q1}\n")
			f.write(f"student_id,target,first_choice,ai_pred,second_choice,time1,time2,time3\n")
		switch_page("tutorial")
		# if st.session_state.group == 0:
		# 	switch_page("vis-xai")
		# else:
		# 	switch_page("lang-xai")

# next_page = st.button("Start", key = 1)
# if next_page:
# 	id = 0
# 	while os.path.exists(str(st.session_state.group) + '_' + str(id)+'.csv'):
# 		id = id + 1
# 	filename = str(st.session_state.group) + '_' + str(id) + '.csv'
# 	st.session_state.filename = filename
# 	with open(filename, 'a+') as f:
# 		f.write(f"Filename,{filename}\n")
# 	if st.session_state.group == 0:
# 		switch_page("vis-xai")
# 	else:
# 		switch_page("lang-xai")

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






