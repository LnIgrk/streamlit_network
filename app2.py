import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
import json
import os
from filelock import FileLock

st.title("Now it's your turn to create a fair network! 😎")


def got_func():
    got_net = Network(height="600px", width="70%", font_color="black", heading=" ")

    # Read data
    got_data = pd.read_csv("data/sample_edges_2.csv")
    sources = got_data['source']
    targets = got_data['target']
    source_groups = got_data['source_group']

    edge_data = zip(sources, targets, source_groups)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        color = "#FF0000" if e[2] == 0 else "#0000FF"

        got_net.add_node(src, src, title=src, color=color)
        got_net.add_node(dst, dst, title=dst, color=color)
        got_net.add_edge(src, dst)

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

got_net = got_func()

with FileLock(lock_path):
    got_net.write_html(file_path)

# Reading and manipulating the HTML file safely
with open(file_path, 'r', encoding='utf-8') as HtmlFile:
    source_code = HtmlFile.read()

# Inject script to capture selected nodes
selection_script = '''
<script type="text/javascript">
    var selected_nodes = [];
    network.on("selectNode", function(params) {
        selected_nodes = params.nodes;
        document.getElementById("selected_nodes").innerText = JSON.stringify(selected_nodes);
    });
</script>
<div id="selected_nodes"></div>
'''

# Combine the original HTML with the injected script
source_code = source_code.replace('</body>', selection_script + '</body>')

# Component to display the network with injected script
components.html(source_code, height=800, width=1000)

# Displaying selected node IDs
st.sidebar.title('Options')
st.sidebar.write('Selected Nodes:')
selected_nodes = st.sidebar.empty()
nodes_placeholder = st.sidebar.empty()

if st.sidebar.button("Show Selected Nodes"):
    nodes_placeholder.text(selected_nodes)

st.sidebar.button("Start again", key=None, help="Click to recreate the initial network", on_click=st.experimental_rerun)