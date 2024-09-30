# To make components
import streamlit as st
# to read CSV files
import pandas as pd
# to handle datetime values
from datetime import datetime
# calendar widget created in widgets.py
from widgets import make_calendar

# ########## HOME VIEW FUNCTION
def homefunc():

    tasks = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)

    # make three columns of equal width
    sections = st.columns(2)

    # call the first column and design the view under
    with sections[0]:
        # make a container with a border. this can hold text and other contents
        tc = st.container(border=True)

        # call top container and insert content
        tc.markdown("<h5>Today's Schedule</h3>", True)
        tc.write(datetime.today().date().strftime("%A, %B %d, %Y"))
        tc.write(f"Welcome, {'Javier Ortiz'}")
        tc.write(f"Your Role: {'Test Engineer'}")

        # call top contatiner and insert calender widget
        calwid = make_calendar()
        calwid

    # call the second column and design the view under
    with sections[1]:
        goals = pd.read_csv("newqueries/Query3_Goals.csv", index_col=0)
        co = st.container(border=True)
        co.markdown("<h5>Goals</h5>", True)

        # target_tasks = tasks[tasks["StudentName"] == "Javier Ortiz"]
        co.markdown(f"**Operation Name:** {'Operation Desert Storm'}")
                    
        co.dataframe(goals.iloc[:, :-1], hide_index=True)


    # call the third container and design the view under
    # with sections[2]:
    #     tc = st.container(border=True, height=350)
    #     bc = st.container(border=True, height=120)

    #     tc.markdown("<h5>Recent Changes</h5>", True)
    #     bc.markdown("<h5>Warnings Summary</h5>", True)

# ########## PROGRAM MANAGEMENT VIEW FUNCTION
def progmgmtfunc():

    # make two columns of width 30% and 60%
    cols = st.columns([0.3, 0.6])

    # get the data for roles and responsibilities
    roles = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)

    # insert a column for roles
    role_dict = dict(zip(roles["StudentName"].value_counts().index, 
                         ["Test Engineer", "Test Engineer", "Systems Architect", "Program Manager", "Software Engineer", "CBTDEV", "Test Engineer"]))
    roles["Role"] = roles["StudentName"].apply(lambda x: role_dict[x])

    # call the first column, and design the view under
    with cols[0]:
        st.markdown("<h6>Assigned Responsibilities</h6>", True)
        st.dataframe(roles[["StudentName", "Role"]].drop_duplicates(ignore_index=True).reset_index(drop=True),
                     hide_index=True, use_container_width=True)

    # call the second column and design the view under
    with cols[1]:
        cont = st.container(border=True, height=600)
        cont.markdown("<h5>Task Overview</h5>", True)
        cont.dataframe(roles[["StudentName", "Description"]],hide_index=True, use_container_width=True)