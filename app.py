import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import numpy as np
import got 
#Network(notebook=True)
st.title("Now it's your turn to create a fair network!")
np.float_ = np.float64
# make Network show itself with repr_html

def net_repr_html(self):
  nodes, edges, height, width, options = self.get_network_data()
  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
  return html


Network._repr_html_ = net_repr_html
st.sidebar.title('Options')
st.sidebar.button("Start again", key=None, help="click to recreate the initial network ", on_click=None, args=None, kwargs=None)

got.got_func()
HtmlFile = open("html_files/sample_test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, height = 1200,width=1000)

# HtmlFile = open("test.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read()
# components.html(source_code, height = 900,width=900)
