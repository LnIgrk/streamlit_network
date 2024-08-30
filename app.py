import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
import json
import os
from filelock import FileLock
# from streamlit_javascript import st_javascript

st.title("Now it's your turn to create a fair network! 😎")

def render_network(got_net, file_path):
    with FileLock(lock_path):
        got_net.write_html(file_path)
    with open(file_path, 'r', encoding='utf-8') as HtmlFile:
        source_code = HtmlFile.read()
    components.html(source_code, height=800, width=1000)

# Function to create the network graph
def got_func():
    got_net = Network(height="600px", width="70%", font_color="black", heading=" ")

    # Read data
    got_data = pd.read_csv("data/sample_edges_2.csv")
    sources = got_data['source']
    targets = got_data['target']
    source_groups = got_data['source_group']

    edge_data = zip(sources, targets, source_groups)

    # Add nodes and edges to the network
    for e in edge_data:
        src = e[0]
        dst = e[1]
        color = "#FF0000" if e[2] == 0 else "#0000FF"

        got_net.add_node(src, src, title=src, color=color)
        got_net.add_node(dst, dst, title=dst, color=color)
        got_net.add_edge(src, dst)

    # Set additional options
    for node in got_net.nodes:
        node["title"] = "Hello"
        node["value"] = 2

    got_net.set_options("""
    var options = {
        "interaction": {
            "multiselect": true,
            "dragView": true,
            "zoomView": true
        }
    }
    """)
    return got_net

# Ensure thread-safety in file write
file_path = "html_files/sample_test.html"
lock_path = os.path.splitext(file_path)[0] + ".lock"

# Get the generated network graph
got_net = got_func()
# Write generated HTML to file
with FileLock(lock_path):
    got_net.write_html(file_path)


@st.fragment
def draw_visual():
    render_network(got_net, file_path)

draw_visual()

from_ = st.sidebar.text_input("Add edge from", value="", )
to_ = st.sidebar.text_input("Add edge to", value="", )

if st.sidebar.button("Add an edge"):
    got_net.add_edge(int(from_), int(to_))
    got_net.write_html(file_path)
    draw_visual()

from_remove = st.sidebar.text_input("Remove edge from", value="", )
to_remove = st.sidebar.text_input("Remove edge to", value="", )

if st.sidebar.button("Remove an edge"):
    edges = got_net.get_edges()
    edges = [edge for edge in edges if not (edge['from'] == int(from_remove) and edge['to'] == int(to_remove))]
    got_net.edges = edges
    got_net.write_html(file_path)
    st.session_state["component_cleared"] = True
    draw_visual()


