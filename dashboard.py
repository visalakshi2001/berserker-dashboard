import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import graphviz
from datetime import datetime, timedelta

from issues import issuesinfo

COLORS = px.colors.qualitative.Plotly


# ########## TEST SCHEDULE VIEW FUNCTION
def dashschedule():
    # Make a heading of size H2
    st.subheader("Schedule", divider="orange")

    # # create two columns of equal size
    # top_columns = st.columns(2)

    # # call the first column and design the view under
    # with top_columns[0]:
    #     # this column will hold the number of tests scheduled, read data for test programs
    #     programs = pd.read_csv("reports/TestPrograms.csv", index_col=0)

    #     st.markdown("<h6>Scheduled Test Programs</h6>", True)
    #     # make 4 sub-columns and display the data using col.metric()
    #     metriccols = st.columns(4)
    #     for i,num in enumerate(programs["num_Tests"]):
    #         metriccols[i].metric(label=programs.iloc[i]["TestProgram"], value=num, delta=f"{num-2} Scheduled")

    # # call the second column and insert the issues section from issues.py
    # with top_columns[1]:
    #     issuesinfo()
    
    sch_opts = ["Test Schedule", "Milestone Schedule"]
    schedule_choice = st.selectbox("Select a schedule to view", options=sch_opts)

    if schedule_choice == sch_opts[0]:
        cols = st.columns([0.55, 0.3])
        breakdown = pd.read_csv("newqueries/TestBreakdown.csv", index_col=0)
        dot = graphviz.Digraph(comment='Hierarchy', strict=True)
        for index, row in breakdown.iterrows():
                tp = row["TestProgram"]
                sub = row["SubTP"]
                event = row["TestEvent"]
                testsubject = row["TestSubject"]
                testcomponent = row["TestComponent"]

                if pd.notna(tp):
                    dot.node(tp)

                if pd.notna(sub):
                    if sub not in dot.body:
                        dot.node(sub)
                    if pd.notna(sub):
                        dot.edge(tp, sub, label="has a type")
                
                if pd.notna(event):
                    if event not in dot.body:
                        dot.node(event)
                        dot.edge(sub, event, label="has test event")  
                # if pd.notna(testsubject):
                #     if testsubject not in dot.body:
                #         dot.node(testsubject, shape="box")
                #         dot.edge(event, testsubject, label="has test subject")  
        cols[0].graphviz_chart(dot, True)
        cols[1].dataframe(breakdown[["TestEvent", "TestSubject", "TestComponent", "Start"]], hide_index=True, use_container_width=True)


        # read the data for test schedule
        # testscheduling = pd.read_csv("reports/Query6_Scheduling 2.csv", index_col=0)
        testscheduling = pd.read_csv("newqueries/Query7_Tests.csv", index_col=0)
        testscheduling["Start"] = pd.to_datetime(testscheduling["Start"])
        # testscheduling["End"] = pd.to_datetime(testscheduling["End"])
        testscheduling["End"] = testscheduling["Start"] + pd.Timedelta(hours=3)
        testscheduling["Site"] = testscheduling["TestEvent"].values

        # Define a function to extract the week of year
        testscheduling['Week'] = testscheduling['Start'].dt.strftime('%Y-W%U')

        # Creating the Plotly figure for timeline chart of test schedule
        fig = px.timeline(testscheduling, x_start="Start", x_end="End", y="Site", color="TestEvent", text="TestSubject", hover_name="TestComponent",
                        category_orders={"Site": sorted(testscheduling['Site'].unique(), key=lambda x: str(x))})

        
        # Update layout to include a dropdown menu for week selection
        week_options = testscheduling['Week'].unique()

        # update the layout with options menu, time-axis scale, etc.
        fig.update_layout(
            title="Test Site Schedule",
            xaxis_title="Time",
            yaxis_title="Test Event",
            xaxis=dict(
                tickformat="%d %b %Y\n%H:%M",
                range=[testscheduling['Start'].min() - pd.Timedelta(days=1), testscheduling['End'].min() + pd.Timedelta(days=6)],
            ),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [
                            {"xaxis.range": [testscheduling[testscheduling['Week'] == week]['Start'].min(), testscheduling[testscheduling['Week'] == week]['End'].max()]}
                        ],
                        "label": week,
                        "method": "relayout"
                    }
                    for week in week_options
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.17,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top"
            }],
            legend=dict(xanchor="left", x=0, y=1, yanchor="bottom", orientation="h"),
            showlegend=False
        )
        vlinedate = datetime.today().date()
        fig.add_vline(x=datetime(vlinedate.year, vlinedate.month, vlinedate.day).timestamp() * 1000, annotation_text= f"today {vlinedate.month}/{vlinedate.day}")
        
        # insert the figure in the view using streamlit
        st.plotly_chart(fig, use_container_width=True)

    
    if schedule_choice == sch_opts[1]:
        decisionreview = pd.read_csv("reports/Query3_Decisions.csv", index_col=0)
        decisionreview['ReviewStart'] = pd.to_datetime(decisionreview['ReviewStart'])
        # Define ReviewEnd as 1 hour after ReviewStart (since no end times are given)
        decisionreview['ReviewEnd'] = decisionreview['ReviewStart'] + pd.Timedelta(hours=1)
        # Define a function to extract the week of year
        decisionreview['Week'] = decisionreview['ReviewStart'].dt.strftime('%Y-W%U')

        # Creating the Plotly figure
        fig = px.timeline(decisionreview, x_start="ReviewStart", x_end="ReviewEnd", y="Review", color="Decision", text="Milestone", hover_name="Milestone",
                        category_orders={"Review": sorted(decisionreview['Review'].unique(), key=lambda x: str(x))})

        # Update layout to include a dropdown menu for week selection
        week_options = decisionreview['Week'].unique()

        fig.update_layout(
            title="Review Schedule",
            xaxis_title="Time",
            yaxis_title="Review",

            updatemenus=[{
                "buttons": [
                    {
                        "args": [
                            {"xaxis.range": [decisionreview[decisionreview['Week'] == week]['ReviewStart'].min() - pd.Timedelta(days=1), decisionreview[decisionreview['Week'] == week]['ReviewEnd'].max() + pd.Timedelta(days=6)]}
                        ],
                        "label": week,
                        "method": "relayout"
                    }
                    for week in week_options
                ],
                "direction": "down",
                "showactive": True,
                "x": 0.17,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top"
            }]
        )
        # insert the created figure in the UI 
        st.plotly_chart(fig, True)

    
def dashresults():
    st.subheader("Performance", divider="violet")
    results = pd.read_csv("newqueries/Query9_TestResults.csv", index_col=0)
    cols = st.columns(4)
    for i,row in results.iterrows():
        if pd.isnull(row["Unit"]): row["Unit"] = "" 
        if pd.isnull(row["MoPUnit"]): row["MoPUnit"] = "" 
        delta_value = "Minimum Performance Value: "+ str(row["MoPValue"]) +"  " + row["MoPUnit"]
        delta_color = "inverse" if row["Value"] < row["MoPValue"] else "normal"

        value = str(row["Value"]) + "  " + row["Unit"]
        cols[i].metric(label="Measurement of " + row["MeasurementOf"], value=value, delta=delta_value, delta_color=delta_color)
    
    cols = st.columns([0.7,0.3])
    cols[0].dataframe(results, hide_index=True, use_container_width=True, height=300)

    with cols[1]:
        cont = st.container(border=True, height=300)
        cont.markdown("<h5>Results Status</h5>", True)

        notimplemented = results[~results["MoPUnit"].isnull()]
        setofwarnings = set()
        for i,row in results.iterrows():
            if pd.isnull(row["MoPUnit"]):
                setofwarnings.add(f'{row["MeasurementOf"]} does not have a measure unit')

            if row["Value"] < row["MoPValue"]:
                setofwarnings.add(f'{row["MeasurementOf"]} Test Value does not pass the requirement limit')
        for warning in setofwarnings:
            cont.warning(warning, icon="⚠️")
    

# ########## TEST SCHEDULE VIEW FUNCTION
def dashresults_obsolete():
    # create a heading of size H2
    st.subheader("Performance", divider="violet")

    # create two columns of sizes 40% and 60%
    top_columns = st.columns([0.4,0.6])

    # call the second column and insert the issues section from issues.py
    with top_columns[1]:
        issuesinfo()
    
    # call the first column and design the view under
    with top_columns[0]:
        resultsdocument = pd.read_csv("reports/DocumentSearch.csv", index_col=0)
        verificationcheck = pd.read_csv("reports/Query7_VerificationCheck.csv", index_col=0)
        
        st.markdown("<h6>Test Data Results</h6>", True)

        metricchoice = st.selectbox("Select Test Data Document", 
                                    options=["Payload Test Data Report", "Verification Results"], index=0)

        if metricchoice == "Payload Test Data Report":
            metriccols = st.columns([1, 1.5, 1.5], gap="small") 
            for index,row in resultsdocument.iterrows():
                with metriccols[index]:
                    value = str(row["Value"]) + " " + str(row["Unit"]) if (pd.isna(row["Unit"]) != True) else str(row["Value"])
                    st.metric(label=row["TestData"], value=value, delta=row["TestDataSubject"], help="Test, followed by result value for given test subject")

        if metricchoice == "Verification Results":
            verificationcheck["UnitSymb"] = verificationcheck["Unit"].replace({"percentage": "%"})
            for index,row in verificationcheck.iterrows():
                value = str(row["Value"]) + " " + str(row["UnitSymb"]) if (pd.isna(row["UnitSymb"]) != True) else str(row["Value"])
                st.metric(label=row["MissionReqName"], value=value, delta="Minimum Value: " + str(row["MinValue"]) + str(row["UnitSymb"]),
                          help=f"Test Name: {row['TestName']} \n Test Output: {row['TestOutput']}")
        
        
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    middle_columns = st.columns([0.7, 0.3])

    with middle_columns[0]:
        keycaprates = pd.read_csv("reports/Query5_KeyCapabilities 2.csv", index_col=0)
        keycaprates["UnitSymbols"] = keycaprates["Unit"].map({"percent": "%", "degrees": "deg", "second": "sec", "kilogram": "kg"})

        fig = go.Figure()
        for i in range(len(keycaprates["KCName"])):
            fig.add_trace(go.Scatter(
                x=[keycaprates["Threshold"][i], keycaprates["Objective"][i]],
                y=[keycaprates["KCName"][i], keycaprates["KCName"][i]],
                mode='lines',
                line=dict(color='gray'),
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=[keycaprates["Threshold"][i]],
                y=[keycaprates["KCName"][i]],
                mode='markers+text',
                marker=dict(size=10, color="blue"),
                name="Threshold" if i==0 else "",
                showlegend=(i==0),
                text=[f"{keycaprates['Threshold'][i]} {keycaprates['UnitSymbols'][i]}"],
                textposition="bottom center",
                hovertemplate=f" <b> Satisfied by:</b> {keycaprates['SatisfiedBy'][i]}" + ""
            ))
            fig.add_trace(go.Scatter(
                x=[keycaprates["Objective"][i]],
                y=[keycaprates["KCName"][i]],
                mode='markers+text',
                marker=dict(size=10, color="red"),
                name="Objective" if i==0 else "",
                showlegend=(i==0),
                text=[f"{keycaprates['Objective'][i]} {keycaprates['UnitSymbols'][i]}"],
                textposition="top center",
                hovertemplate=f" <b> Satisfied by:</b> {keycaprates['SatisfiedBy'][i]}" + ""
            ))

        fig.update_layout(title="Threshold vs Objective for Each Key Capacities",
                            xaxis_title="Value",
                            yaxis_title="KCName",
                            yaxis=dict(tickmode='linear'),
                            legend=dict(orientation="h", x=0.3, y=10))

        st.plotly_chart(fig, use_container_width=True)
    
    with middle_columns[1]:
        keycaprates["VerificationStatus"] = np.where(pd.notnull(keycaprates["VerificationMethodName"]),  "Verified", "Unverified")
        
        fig = go.Figure(data=[
            go.Bar(name="Satisfied", y=keycaprates["KCName"], x=np.where(pd.notnull(keycaprates["SatisfiedBy"]), 1, 0),
                    orientation="h", marker=dict(color=COLORS[2]), text=keycaprates["SatisfiedBy"]),
            go.Bar(name="Verified", y=keycaprates["KCName"], x=np.where(pd.notnull(keycaprates["VerificationMethodName"]), 1, 0),
                    orientation="h",marker=dict(color=COLORS[0]), text=keycaprates["VerificationMethodName"])
        ])
        fig.update_layout(barmode="stack",
                            title="Key Capabilities Verification and Satisfaction Status")
        fig.update_traces(textposition="inside", textfont_size=16)
        fig.update_xaxes(showticklabels=False)
        st.plotly_chart(fig, True)



##########################################################################################################
# REFERENCES  # 
#  hover templates: https://plotly.com/python/hover-text-and-formatting/ #
#  scatterplot annotations: https://stackoverflow.com/questions/71875067/adding-text-labels-to-a-plotly-scatter-plot-for-a-subset-of-points #
##########################################################################################################

# ########## REQUIREMENTS VIEW FUNCTION
def dashreqs():
    reqtypes = ["System Requirements", "Mission Requirements"]
    selected_measure = st.selectbox("Select Requirements", options=reqtypes, index=0)

    if selected_measure == reqtypes[0]:
        # cols = st.columns([0.7, 0.3])
        systemreq = pd.read_csv("newqueries/Query8_Requirements.csv", index_col=0)
        # with cols[0]:
        st.dataframe(systemreq, hide_index=True, use_container_width=True)
    
    if selected_measure == reqtypes[1]:
        # cols
        missionreq = pd.read_csv("newqueries/Query8_Requirements2.csv", index_col=0)
        st.dataframe(missionreq, hide_index=True, use_container_width=True, height=250)




def dashreqs_obsolete():
    # read the data for requirements
    reqs = pd.read_csv("reports/Requirements_Rover.csv", index_col=0)

    # Make a dropdown select menu, with options as all the name of Requirements
    req_choice = st.selectbox("Select a Requirement", options=reqs["ReqName"].sort_values().tolist())

    # make three columns of equal width
    cols = st.columns(3)

    # filter the target requirement from the data of all requirement, using the selected requirement name
    # this comes from the name chosen by the user
    target_req = reqs[reqs["ReqName"] == req_choice]

    # initiate empty diagraph chart
    dot = graphviz.Digraph(comment='Hierarchy', strict=True)

    # call the first column and create the chart below
    with cols[0]:
        for index, row in target_req.iterrows():
            requirement = row['ReqName']
            satisfiedby = row['SatisfiedBy']
            verifiedby = row['VerifiedName']
            
            # Add the function node
            dot.node(requirement)
            
            # Add edge from SuperFunction to Function if SuperFunction exists
            if pd.notna(satisfiedby):
                if satisfiedby not in dot.body:
                    dot.node(satisfiedby, shape='box')
                dot.edge(requirement, satisfiedby, label="satisfied by")
            
            # Add AllocatedTo node and edge if it doesn't already exist
            if pd.notna(verifiedby):
                if verifiedby not in dot.body:
                    dot.node(verifiedby, shape='box')
                dot.edge(requirement, verifiedby, label="verified by system")
        st.graphviz_chart(dot)

    # call the second column and display the target requirement information in a table
    with cols[1]:
        st.dataframe(target_req[["ReqName", "SatisfiedBy", "VerifiedName"]], 
                     hide_index=True, height=100, use_container_width=True)
    
    # call the third column and display additional details on the requirement, 
    # along with warnings if applicable
    with cols[2]:
        # make a container of height 420px
        cont = st.container(border=True, height=420)

        # make a heading
        cont.markdown("<h5>Requirement Details & Satisfaction Status</h5>", True)

        # write the details of the target requirement
        cont.markdown(f"""
        **ReqID:** {target_req["ReqID"].iloc[0]} \n 
        **Requirement Name:** {target_req["ReqName"].iloc[0]} \n
        **Description:** {target_req["ReqText"].iloc[0]} \n
        """, True)

        # check for satisfaction and verification details and raise warning if not fulfilled
        satisfied, verified = False, False
        if pd.notnull(target_req["SatisfiedBy"].iloc[0]):
            cont.markdown(f"**Satisfied By:** {target_req['SatisfiedBy'].iloc[0]} \n", True)
            satisfied = True
        if pd.notnull(target_req["VerifiedName"].iloc[0]):
            cont.markdown(f"**Verified By:** {target_req['VerifiedName'].iloc[0]} \n", True)
            verified = True
        
        # raise warning
        if not satisfied:
            cont.warning('This Requirement is not satisfied by any System', icon="⚠️")
        if not verified:
            cont.warning('This Requirement is not verified by any Test/Activity', icon="⚠️")
        if not (satisfied or verified):
            cont.info("See Test Results OR Grading Wizard for all warnings/issues")



def dashmeasures():
    measures = ["Measure of Success", "Measure of Performance", "Measure of Effectiveness"]
    selected_measure = st.selectbox("Select Measureof", options=measures, index=1)

    if selected_measure == measures[1]:
        measures = pd.read_csv("newqueries/Query6_Measures.csv", index_col=0)
        cols = st.columns([0.8, 0.25])
        cols[0].dataframe(measures.style \
                    .apply(lambda x: ["background-color: rgb(244 215 60);"]*len(x) 
                            if pd.isnull(x["MeasureUnit"]) and x["MeasureDim"] not in ["Dimensionless", "Time", "Probability", "Boolean"]
                            else [None]*len(x), axis=1),
                    hide_index=True, use_container_width=True)
        with cols[1]:
            cont = st.container(border=True, height=420)
            cont.markdown("<h5>Measures of Performance Status</h5>", True)

            notimplemented = measures[~measures["MeasureDim"].isin(["Dimensionless", "Time", "Probability", "Boolean"]) & measures["MeasureUnit"].isnull()]
            for i,row in notimplemented.iterrows():
                cont.warning(f'{row["MeasureName"]} does not have a measure unit', icon="⚠️")