############################################################ SETUP ############################################################

############################################################ Imports

import os
import sys
import io
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page

import os

import requests

import math
import pandas as pd
import numpy as np
import json
import random
import re
from collections import Counter
from PIL import Image
import time

## TimeStamp

time_first = str(time.time())

############################################################ Settings

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

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
		div[data-testid="stSidebarNav"] {display: none;}
	</style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# hides button to close sidebar, open settings
no_button_style = """
	<style>
		button[kind="header"] {display:none;}
	</style>
"""
st.markdown(no_button_style, unsafe_allow_html=True)

############################################################ load data

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
	# tutorial student
	student_id = st.session_state.student_id_tutorial
	comprehension = st.session_state.comprehension
	#indexes = st.session_state.indexes
	#explanations_num = st.session_state.x_num
	
except:
	st.session_state.reroute_error = True
	switch_page("Home")

############################################################ Public variables

show_prediction = True
debug = False

############################################################ Public functions


def first_comprehension():
	if comp_1 == "good": # correct!
		st.session_state["state_num"] = 2
		st.session_state.comprehension = True
	else:
		if comprehension: # as of now no failure
			st.session_state.comprehension = False # but the next one has to be correct
		else: # this is the second failure
			st.session_state["state_num"] = -1
			state_num = -1

def second_comprehension():
	if comp_2 == "have a negative impact on the predicted probability": # correct!
		st.session_state["state_num"] = 4
		st.session_state.comprehension = True
	else:
		if comprehension: # as of now no failure
			st.session_state.comprehension = False # but the next one has to be correct
		else: # this is the second failure
			st.session_state["state_num"] = -1
			state_num = -1



def first_decision_submit(student_number):
	st.session_state["time_first"] = time_first
	st.session_state["time_second"] = str(time.time())
	st.session_state["state_num"] = 3
	st.session_state["first_choice"] = choice_1

def final_decision_submit(student_number):
	first_choice = st.session_state["first_choice"]
	second_choice = choice_2
	correct_choice = AI_predictions[str(student_id)]["target"]
	ai_pred = AI_predictions[str(student_id)]["prediction"]
	if second_choice == correct_choice:
		if not "num_correct" in st.session_state:
			st.session_state["num_correct"] = 1
		else:
			st.session_state["num_correct"] = st.session_state["num_correct"] + 1
	#else:
	#	st.write(correct_choice, choice)
	time1 = st.session_state["time_first"]
	time2 = st.session_state["time_second"]
	time3 = str(time.time())
	with open(filename, 'a+') as f:
		f.write(f"tutorial_{student_id},{correct_choice},{first_choice},{ai_pred},{second_choice},{time1},{time2},{time3}\n")

	st.session_state["state_num"] = 1
	st.session_state.tutorial_done = True

# def explanation_cols_as_list(explanation_columns):
# 	explanation_columns = explanation_columns.replace('[\'', '').replace('\']', '').replace(' \'', ' ').replace('\',', ',')
# 	explanation_columns = explanation_columns.replace('["', '').replace('"]', '').replace(' "', ' ').replace('",', ',')
# 	explanation_columns = explanation_columns.split(", ")
# 	return explanation_columns

# def explanation_sublists_as_list(explanation_columns):
# 	explanation_columns_new = []
# 	explanation_columns = explanation_columns[2:-2]
# 	explanation_columns = explanation_columns.split("], [")
# 	for e in explanation_columns:
# 		e = e.split(", ")
# 		e = [ee.strip('\'').strip('"') for ee in e]
# 		e = [ee for ee in e if not ee == ""]
# 		if not e == []:
# 			explanation_columns_new.append(e)
# 	return explanation_columns_new

# def highlight(row): 

# 	highlight_grad = [144, 238, 144]
# 	highlight_drop = [240, 128, 128]
# 	default = ''

# 	row_student = row.name
# 	row_student_num = int(row_student.split()[-1])-1
# 	explanation_columns_num = explanation_cols_as_list(df_full.loc[indexes[student_num]]["explanation_num"])
# 	explanation_columns_cat = explanation_sublists_as_list(df_full.loc[indexes[student_num]]["explanation_cat"])
# 	explanation_columns_cat = {e[0]:e[2] for e in explanation_columns_cat}
# 	ai_pred = df_full.loc[indexes[row_student_num]]["AI prediction"].upper()

# 	highlights = []
# 	for c in row.index:
# 		if c in explanation_columns_num:
# 			if ai_pred == "GRADUATE": #explanations_num[c] == "high" and 
# 				highlights.append(f'background-color: rgba({highlight_grad[0]},{highlight_grad[1]},{highlight_grad[2]},1)')
# 			else:
# 				highlights.append(f'background-color: rgba({highlight_drop[0]},{highlight_drop[1]},{highlight_drop[2]},1)')
# 		elif c in explanation_columns_cat:
# 			opacity = explanation_columns_cat[c]
# 			opacity = float(opacity) - 0.1
# 			opacity = min(opacity*2,1)
# 			opacity = str(opacity)
# 			if ai_pred == "GRADUATE":
# 				highlights.append(f'background-color: rgba({highlight_grad[0]},{highlight_grad[1]},{highlight_grad[2]},{opacity})')
# 			else:
# 				highlights.append(f'background-color: rgba({highlight_drop[0]},{highlight_drop[1]},{highlight_drop[2]},{opacity})')
# 		else:
# 			highlights.append(default)

# 	return highlights

############################################################ MAIN ############################################################

if state_num == -1:
	switch_page("failure")

if st.session_state.tutorial_done == True:
	if st.session_state.group == 0:
		switch_page("vis-xai")
	else:
		switch_page("lang-xai")

############################################################ text

st.markdown("### Graduate or Dropout?")

st.markdown(f'''Here you will be shown 12 sets of student information collected at a portuguese university. Your task is to predict for each student whether they will graduate or drop out.
Below, you can see the student's file with various information about their person and academic career. You will be shown the prediction of our AI system to aid you in making your decision.


---''')

st.warning("This first student is a kind of tutorial so that you can familiarize yourself with how the task will work. In addition to submitting your decision (graduate or dropout) for this student, you will have to solve two comprehension tests, to ensure that you have understood correctly what you should do. You will have two tries on each of these comprehension tests to get the answer right. First, have a look at the student's data below:")


############################################################ display student data

# Printing the chosen random order and student data for debugging purposes
if debug:
	st.write(df)
	st.write(st.session_state.student_order)

# if st.session_state["student_num"] == len(student_order):
# 	st.write("Go to next page")
# 	switch_page("Questionnaire")

#style = df.style.hide_index()
#style.hide_columns()
#style = df.style.format(index='st.session_state.indexes[student_num]', precision=3)
#st.write(style.to_html(), unsafe_allow_html=True)
#st.write(df)
#st.write(indexes)
#df_show = pd.DataFrame(df, index  = indexes)
#st.write(df_show)
#st.write(df_show2.to_html(header=False))

#st.table(df.loc[st.session_state.indexes[student_num]])

#st.dataframe(df.loc[st.session_state.indexes[student_num]], use_container_width=True)
#st.dataframe(df_full.loc[st.session_state.indexes[student_num]], use_container_width=True)

st.markdown(f"**Student {student_id}**")
col1, col2 = st.columns([1,1])
with col1:
#if True:
	#st.dataframe(df.T.loc[:, df.T.columns=="Student " + str(student_num +1) ], use_container_width=True)
	#student_table = df.T.loc[:, df.T.columns=="Student " + str(student_num +1) ]
	#student_table = student_table.style.apply(highlight, axis=0)
	student_table = df.loc[[student_id]].T
	features_grades = [f for f in student_table.index if "semester" in f]
	features_demo = [f for f in student_table.index if not f in features_grades]

	#student_table = df[]
	st.write("Demographic Data")
	st.table(student_table.loc[features_demo])
with col2:
	st.write("Classes & Grades")
	st.table(student_table.loc[features_grades])
	# st.dataframe(
	#     student_table,
	#     column_config={
	#         str(student_id): st.column_config.Column(
	#             width="large"
	#         )
	#     }
	# )

	with st.expander("Grades in Portuguese University System", expanded = (student_num==0)):

		st.info('''
			
		| Portuguese Grade| Grade Description                 | US Grade |
		|---------------|---------------------------------------|--------------|
		| 20.00         | Very good with distinction and honors | A+           |
		| 18.00 - 19.99 | Excellent                             | A+           |
		| 16.00 - 17.99 | Very Good                             | A            |
		| 14.00 - 15.99 | Good                                  | B            |
		| 10.00 - 13.99 | Sufficient                            | C            |
		| 1.00 - 9.99   | Poor                                  | F            |

		''')

#st.write(state_num)

# first comprehension test:
if state_num == 1:
	st.warning("""Now, please solve this comprehension test. The purpose of this question is to ensure that you have understood how to read the student data.   \nPlease re-read the student data tables and the additional information (in blue) if you are unsure.""")
elif state_num > 1:
	st.write("""Now, please solve this comprehension test. The purpose of this question is to ensure that you have understood how to read the student data.   \nPlease re-read the student data tables and the additional information (in blue) if you are unsure.""")
comp_1 = st.radio('Based on the student data you have read above, what grade did the student achieve in their second semester?', ["", "very good", "sufficient", "poor", "good"], key = "comp1", disabled = (state_num != 1))
if state_num == 1 and not comprehension:
	st.write("Please rethink your answer. You have one more chance to answer correctly.")
st.button("Submit", disabled = ((len(comp_1) == 0) or (state_num != 1)), key = "comp_1_submit", on_click = first_comprehension)

# first shot:
if state_num >= 2:

	if state_num == 2:
		st.warning("""Next, please submit your initial prediction of whether this student will graduate or drop out.""")
	else:
		st.write("""Next, please submit your initial prediction of whether this student will graduate or drop out.""")
	
	st.write("""After making your initial decision, you will be able to see the AI suggestion and its explantion, and then submit your final choice.   
		Only your final choice counts for your score.""")

	choice_1 = st.radio("What is your prediction for this student's academic career?", ["", "GRADUATE", "DROPOUT"], key = "decision_choice_1_"+ str(student_num), disabled = (state_num != 2))
	st.button("Enter decision and show AI analysis",disabled = ((len(choice_1) == 0) or (state_num != 2)), key="first_submit", on_click=first_decision_submit, args = (0,))

# AI

if state_num >= 3:

	st.markdown("**AI Analysis**")

	col1, col2 = st.columns([4,2])
	with col1:
	#with col2:

		ai_pred = AI_predictions[str(student_id)]["prediction"]
		ai_probability = AI_predictions[str(student_id)]["grad_prob"]


		#explanation_columns_num = explanation_cols_as_list(df_full.loc[indexes[student_num]]["explanation_num"])
		#explanation_columns_cat = explanation_sublists_as_list(df_full.loc[indexes[student_num]]["explanation_cat"])

		if ai_pred == "DROPOUT":
			st.error("AI prediction\: " + ai_pred + " (Probability of graduation: " + str(ai_probability) + ")")
			h = "red"
		else:
			st.success("AI prediction\: " + ai_pred + " (Probability of graduation: " + str(ai_probability) + ")")
			h = "green"

		with st.expander("How the AI works", expanded = (student_num==0)):

		#st.write("How the AI works:")
			st.info('''Based on all of the factors known about the student, the AI calculates how likely it is that this student will graduate. Some factors positively influence the prediction (meaning they make it more likely for the student to graduate), others influence it negatively.
				
Students have a base chance of graduation of 61%, meaning that an average student will graduate with a probability of 61%. If for a given student there are enough factors that negatively influence their likelihood to graduate, the probability might drop below 50%, meaning they will likely drop out.

The explanation below details how the most important factors (those with an impact greater than 1% in the positive or negative direction) influenced the AI prediction.''')

		

	with col2:

		pass

		#explanation = f"Explanation:   \n   The information that contributed the most to this prediction is highlighted in {h} in the table on the left. The highlighted values were important in comparison to similar students in the training dataset. Here, the most important factors were:"
		
		# for e in explanation_columns_num:
		# 	d = explanations_num[e]
		# 	if ai_pred.upper() == "DROPOUT":
		# 		if d == "high": d = "low"
		# 		elif d == "low": d = "high"
		# 	explanation += "   \n   - **" + d +"** value in **"+e+"**"

		# for e in explanation_columns_cat:
		# 	explanation += "   \n   - **" + e[0] + "** is **" + e[1] + "**"# + e[2]
		
		#if ai_pred.upper() == "DROPOUT":
		#	st.error(explanation)
		#else:
		#	st.success(explanation)

	st.write("Explanation:")
	if st.session_state.group == 0:
		explanation_path = os.path.join(project_path, 'data/explanations_vis/'+str(student_id)+'.png')
		expImage = Image.open(explanation_path) 
		st.image(expImage)
	else:
		explanation = AI_predictions[str(student_id)]["text"]
		st.write("Explanation   \n\n"+explanation)

	if state_num == 3:
		st.warning('''Before you submit your final decision, please solve this second comprehension test.   \nPlease re-read the student data tables, the additional information (in blue), as well as the explanation of the AI prediction if you are unsure.''')
	comp_2 = st.radio('Based on the student data and the AI analysis you have read above, did the gender of the student...', ["", "not have an influence on the predicted graduation probability", "have a positive impact on the predicted probability", "have a negative impact on the predicted probability"], key = "comp2", disabled = (state_num != 3))
	if state_num == 3 and not comprehension:
		st.write("Please rethink your answer. You have one more chance to answer correctly.")
	st.button("Submit", disabled = ((len(comp_2) == 0) or (state_num != 3)), key = "comp_2_submit", on_click = second_comprehension)

if state_num >= 4:

	st.warning('''Now you can submit your final decision on wether this student will graduate or drop out, taking into account the AI analysis.   \nAfter you submit your choice, you will make decisions on 11 more students.''')

	st.write("Please make your final choice here, taking into account the AI analysis.")
	choice_2 = st.radio("What is your prediction for this student's academic career?", ["", "GRADUATE", "DROPOUT"], key = "decision_choice_2_"+ str(student_num), disabled = (state_num < 4))
	st.button("Confirm decision",disabled = (len(choice_2) == 0 or (state_num < 4)),key="second_submit", on_click=final_decision_submit, args = (0,))

	

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