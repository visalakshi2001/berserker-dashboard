import streamlit as st
import pandas as pd

# for making UML diagrams
import graphviz


# ########## ARCHITECTURE VIEW FUNCTION
def sysarcfunc():
    # read the data for the architecture
    # function = pd.read_csv("reports/FunctionalArchitecture.csv", index_col=0)
    # system = pd.read_csv("reports/Query2_SystemArchitecture.csv", index_col=0)
    # mission = pd.read_csv("reports/Query1_MissionArchitecture 1.csv", index_col=0)
    function = pd.read_csv("newqueries/Query5_Functions.csv", index_col=0)
    system = pd.read_csv("newqueries/Query4_SoIArchitecture.csv", index_col=0)
    environment = pd.read_csv("reports/Environment.csv", index_col=0)
    mission = pd.read_csv("newqueries/Query1_MissionArchitecture.csv", index_col=0)
    missionarch = pd.read_csv("newqueries/Query2_MissionStructure.csv", index_col=0)
    moe = pd.read_csv("reports/Query4_MOEs.csv", index_col=0)

    # Make a dropdown selection menu, with a title, and list of options. 
    # this component returns the variable that is selected
    graphchoice = st.selectbox("Select view", ["Function Allocation", "System Architechture", "Missions",
                                               "Mission Architecture", "MOE", "Environments"], index=2)

    # initiate a empty diagraph
    dot = graphviz.Digraph(comment='Hierarchy', strict=True)
    
    # take each option, and design the graph, if the option is selected
    if graphchoice == "Function Allocation":
        
        subcols = st.columns([0.65,0.30])
        function_copy = function.copy()
        subcols[0].dataframe(function.sort_values(["MissionThread"], ascending=False).style. \
                       apply(lambda x: ["background-color: rgb(244 215 60);"]*len(x) if pd.isnull(x["MissionTask"]) 
                             else (
                                 ["background-color: #90ee90;"]*len(x) if ("USA" in x["MissionThread"]) 
                                 else (
                                     ["background-color: salmon;"]*len(x) if ("IRQ" in x["MissionThread"])
                                     else [None]*len(x)
                                 )
                             ), axis=1), 
                       hide_index=True, use_container_width=True, height=500)

        with subcols[1]:
            cont = st.container(border=True, height=420)

            # make a heading
            cont.markdown("<h5>Functional Allocation Status</h5>", True)

            notimplemented = function[function["Function"].notnull() & function["MissionTask"].isnull()]
            for i,row in notimplemented.iterrows():
                cont.warning(f'Function {row["Function"]} is not implemented by any Mission Task', icon="⚠️")   
    
    elif graphchoice == "System Architechture":
        showtab = st.checkbox("Show tabular view for subsubsystem")
        if showtab:
            dot = graphviz.Digraph(comment='Hierarchy', strict=True, graph_attr={'rankdir':'LR'}, 
                                   node_attr={ "fontsize": "20pt"})
            for index, row in system.iterrows():
                sys = row["SystemName"]
                subsys = row["Subsystem"]

                if pd.notna(sys):
                    dot.node(sys)

                if pd.notna(subsys):
                    if subsys not in dot.body:
                        dot.node(subsys)
                    if pd.notna(sys):
                        dot.edge(sys, subsys, label="has subsystem")
            st.graphviz_chart(dot, True)

            pivot_system = system.pivot_table(index="Subsystem", columns="Subsubsystem", aggfunc=lambda x: True, fill_value=False)
            pivot_system.index.name = None
            pivot_system.columns = pivot_system.columns.droplevel()
            st.dataframe(pivot_system)
        else:
            dot = graphviz.Digraph(comment='Hierarchy', strict=True, graph_attr={'rankdir':'LR'})
            for index, row in system.iterrows():
                sys = row["SystemName"]
                subsys = row["Subsystem"]
                subsubsys = row["Subsubsystem"]

                if pd.notna(sys):
                    dot.node(sys)

                if pd.notna(subsys):
                    if subsys not in dot.body:
                        dot.node(subsys)
                    if pd.notna(sys):
                        dot.edge(sys, subsys, label="has subsystem")
                
                if pd.notna(subsubsys):
                    if subsubsys not in dot.body:
                        dot.node(subsubsys, shape="box")
                    if pd.notna(subsys):
                        dot.edge(subsys, subsubsys, label="has subsubsystem")  
            st.graphviz_chart(dot, True)
    
    elif graphchoice == "Environments":
        for index, row in environment.iterrows():
            mission = row["Mission"]
            env = row["Environment"]
            entity = row["EnvironmentalEntity"]

            dot.node(mission)

            if pd.notna(env):
                dot.edge(mission, env, label="has environment")
            if pd.notna(entity):
                dot.edge(env, entity, label="has environment entity")
        st.graphviz_chart(dot, True)
    
    elif graphchoice == "Missions":
        for index, row in  mission.iterrows():
            operation = row["OperationName"]
            missname = row["MissionName"]
            missphase = row["MissionPhaseName"]
            missvignette = row["MissionVignetteName"]


            dot.node(operation)

            if pd.notna(missname):
                if missname not in dot.body:
                    dot.node(missname)
                dot.edge(operation, missname, label="has mission")
            if pd.notna(missphase):
                dot.node(missphase)
                dot.edge(missname, missphase, label="has mission phase")
            if pd.notna(missvignette):
                dot.node(missvignette, shape="box")
                dot.edge(missphase, missvignette, label="mission vignette")
        st.graphviz_chart(dot, True)

        # for index, row in  mission.iterrows():
        #     program = row["ProgramName"]
        #     missname = row["MissionName"]
        #     misscomp = row["MissionComponentName"]
        #     subsys = row["SubsystemName"]

        #     dot.node(program)

        #     if pd.notna(missname):
        #         if missname not in dot.body:
        #             dot.node(missname)
        #         dot.edge(program, missname, label="has mission")
        #     if pd.notna(misscomp):
        #         dot.node(misscomp, shape="box")
        #         dot.edge(missname, misscomp, label="has component")
        #     if pd.notna(subsys):
        #         dot.edge(misscomp, subsys,  label="has subsystem")
    elif graphchoice == "Mission Architecture":
        for index, row in  missionarch.iterrows():
            operation = row["OperationName"]
            missname = row["MissionName"]
            system = row["System"]

            dot.node(operation)

            if pd.notna(missname):
                if missname not in dot.body:
                    dot.node(missname)
                dot.edge(operation, missname, label="has mission")
            if pd.notna(system):
                dot.node(system, shape="box")
                dot.edge(missname, system, label="has system")
        st.graphviz_chart(dot, True)
    elif graphchoice == "MOE":
        for index, row in moe.iterrows():
            missname = row["MissionName"]
            moename = row["MOEName"]

            dot.node(missname)

            if pd.notna(moename):
                dot.edge(missname, moename, label="has moe")
        st.graphviz_chart(dot, True)
    




