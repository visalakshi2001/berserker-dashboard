import streamlit as st
# library for creating calendar widget
from streamlit_calendar import calendar
import pandas as pd

# this code comes from the documentation
# https://github.com/im-perativa/streamlit-calendar


def get_task_list():
    tasks = pd.read_csv("reports/Tasks_Rover.csv", index_col=0)

    target_tasks = tasks[tasks["StudentName" == "Javier Ortiz"]]

    for i,row in target_tasks.iterrows():
        pass


def make_calendar(view="dayGridDay", static=False):
    calendar_options = {
        "initialView": "dayGridDay",
        "editable": "true",
        "selectable": "true",
        "navLinks": "true",
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "18:00:00",
        "titleFormat": {
            "month": "short",
            "day": "numeric",
            "year": "2-digit"
        }
    }
    calendar_events = [
        {
            "title": "TE-2, MQ-99_Berserker, AircraftTestArena",
            "start": "2024-09-26T12:00:00",
            "end": "2024-09-26T15:00:00",
            "resourceId": "MQ-99_Berserker",
        },
        {
            "title": "Event 2",
            "start": "2024-09-11T07:30:00",
            "end": "2024-09-11T10:30:00",
            "resourceId": "b",
        },
        {
            "title": "Event 3",
            "start": "2024-09-12T10:40:00",
            "end": "2024-09-12T12:30:00",
            "resourceId": "a",
        }
    ]

    custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 1rem;
        }
"""

    calendar_widget = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
    return calendar_widget