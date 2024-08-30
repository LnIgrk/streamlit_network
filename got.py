import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st


def got_func(physics=None):
  got_net = Network(height="600px", width="70%", font_color="black", heading=" ")

# set the physics layout of the network
  got_net.barnes_hut()
  got_data = pd.read_csv("data/sample_edges_2.csv")
  sources = got_data['source']
  targets = got_data['target']
  source_groups = got_data['source_group']
  # weights = got_data['Weight']

  edge_data = zip(sources, targets, source_groups)

  for e in edge_data:
    src = e[0]
    dst = e[1]
    color = "#FF0000" if e[2]==0 else "#0000FF"
    # w = e[2]

    got_net.add_node(src, src, title=src, color=color)
    got_net.add_node(dst, dst, title=dst, color=color)
    got_net.add_edge(src, dst)

  # neighbor_map = got_net.get_adj_list()
  # add neighbor data to node hover data
    for node in got_net.nodes:
      node["title"] = "Hello"
      node["value"] = 2
  # if physics:
  #   got_net.show_buttons(filter_=['physics'])

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
  # got_net.show("html_files/sample_test.html")

# got_func()
# print("hello")

