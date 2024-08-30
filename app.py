import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
import json
import os
from filelock import FileLock
from streamlit_javascript import st_javascript

st.title("Now it's your turn to create a fair network! 😎")

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
        print(got_net.get_nodes())
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

# Read HTML content of the network graph
with open(file_path, 'r', encoding='utf-8') as HtmlFile:
    source_code = HtmlFile.read()

# Inject script to capture selected nodes
# selection_script = """
# <input id="selected_nodes" value="[]">
# <script type="text/javascript">
#     var selected_nodes = [];
#     var network; // Assuming 'network' is already initialized elsewhere in your code
#
#     network.on("selectNode", function(params) {
#         selected_nodes = params.nodes;
#         document.getElementById("selected_nodes").value = JSON.stringify(selected_nodes);
#         console.log('Selected Node IDs:', selected_nodes);
#     });
# </script>
# """

# Combine the original HTML with the injected script
# source_code = source_code.replace('</body>', selection_script + '</body>')

# Display network graph in Streamlit with HTML and JavaScript
components.html(source_code, height=800, width=1000)

# Adding JavaScript code to read from hidden input and send its value to Streamlit
# js_code = """
# (async function() {
#     const sleep = (t) => new Promise((s) => setTimeout(s, t));
#
#     while (true) {
#         var selectedNodes = document.getElementById("selected_nodes").value;
#         console.log(selectedNodes)
#         await Streamlit.setComponentValue(selectedNodes);
#         await sleep(1000);  // Check every second
#     }
# })();
# """

from_ = st.sidebar.text_input("Add edge from", value="", )
to_ = st.sidebar.text_input("Add edge to", value="", )

from_remove = st.sidebar.text_input("Remove edge from", value="", )
to_remove = st.sidebar.text_input("Remove edge to", value="", )
# Capture selected nodes dynamically and send to Streamlit
# selected_nodes = st_javascript(js_code)
# print(selected_nodes)

if st.sidebar.button("Show Selected Nodes"):
    # selected_nodes = st_javascript(js_code)
    # st.sidebar.write("Selected Nodes: " + str(selected_nodes))
    st.sidebar.write(f"from {from_} to {to_}")

if st.sidebar.button("Add an edge"):
    # selected_nodes = st_javascript(js_code)
    # st.sidebar.write("Selected Nodes: " + str(selected_nodes))
    got_net.add_edge(from_, to_)

if st.sidebar.button("Remove an edge"):
    # selected_nodes = st_javascript(js_code)
    # st.sidebar.write("Selected Nodes: " + str(selected_nodes))
    edges = got_net.get_edges()
    edges = [edge for edge in edges if not (edge['from'] == from_remove and edge['to'] == to_remove)]
    got_net.edges = edges
    got_net.show("html_files/sample_test.html")
# Convert JSON string from selected_nodes to list
# if selected_nodes:
#     selected_nodes_list = json.loads(selected_nodes)
# else:
#     selected_nodes_list = []

# Display selected nodes in the sidebar
# st.sidebar.write("Selected Nodes: " + str(selected_nodes))