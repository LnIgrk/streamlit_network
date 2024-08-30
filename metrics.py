import networkx as nx
import numpy as np
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
import numpy as np
import pandas as pd
import pandas as pd

"""Common-Language Effect Size"""


def cles(lessers, greaters):
    """Common-Language Effect Size

    Probability that a random draw from `greater` is in fact greater
    than a random draw from `lesser`.

    Args:
      lesser, greater: Iterables of comparables.
    """
    if len(lessers) == 0 and len(greaters) == 0:
        raise ValueError('At least one argument must be non-empty')
    # These values are a bit arbitrary, but make some sense.
    # (It might be appropriate to warn for these cases.)
    if len(lessers) == 0:
        return 1
    if len(greaters) == 0:
        return 0
    numerator = 0
    lessers, greaters = sorted(lessers), sorted(greaters)
    lesser_index = 0
    for greater in greaters:
        while lesser_index < len(lessers) and lessers[lesser_index] < greater:
            lesser_index += 1
        numerator += lesser_index  # the count less than the greater
    denominator = len(lessers) * len(greaters)
    return float(numerator) / denominator

def gini(G):
    g = 0

    E = len(G.edges())
    N = len(G.nodes())
    avg_degree = 0

    for n1 in G.nodes():
        avg_degree += G.degree(n1)
        for n2 in G.nodes():
            if n1 == n2:
                continue

            g += abs(G.degree(n1) - G.degree(n2))

    avg_degree = avg_degree / N

    g = g / (2 * N**2 * avg_degree)

    return g

def EI(G):
    internal = 0
    external = 0

    for u,v in G.edges():
        g1 = G.nodes[u]['m']
        g2 = G.nodes[v]['m']

        if g1 == g2:
            internal += 1
        else:
            external += 1

    return (external - internal) / (external + internal)

def inequity(G):

    g1 = []
    g2 = []

    for n,data in G.nodes(data=True):
        if data['m'] == 0:
            g1.append(G.degree(n))
        else: 
            g2.append(G.degree(n))

    return cles(g1,g2)

def write_csv(G):
    
    with open('network.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['source', 'target', 'source_group', 'target_group'])
        
        for u,v in G.edges():
            spamwriter.writerow([u,v, G.nodes[u]['m'], G.nodes[v]['m']])

def parse_csv(path):

    G = nx.Graph()

    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            G.add_edge(row['source'], row['target'])
            G.nodes[row['source']]['m'] = int(row['source_group'])
            G.nodes[row['target']]['m'] = int(row['target_group'])

            #print(row['source'], row['target'])

    return G

def plot_network(df, G, ax=None):
    num_rows = len(df)
    num_circles = len(df.columns)
    circle_radius = 0.015  # Small radius for the circles
    fig_height = max(4, num_rows * 0.6)  # Ensure minimum height and scale by number of rows
    if ax == None:
        fig, ax = plt.subplots(figsize=(8, fig_height), facecolor="CornflowerBlue")
    else:
        fig = None

    line_length = 0.1

    # Correctly ordered and unique color thresholds
    thresholds = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

    def get_grey_scale_color(value):
        # Compare value against custom thresholds and assign a color
        colors = ['#5882CF','#4B70B2', '#3F5D94', '#324B77', '#263859', '#19253B', '#0D131E']  # Light to dark grey
        for idx, threshold in enumerate(thresholds):
            if value <= 0.0:
                return '#6495ED'
            if value <= threshold:
                return colors[idx]
        return colors[-1]  # Darkest color for anything above the highest threshold

    def get_red_scale_color(value):
        # Compare value against custom thresholds and assign a color
        colors = ['#8B81B2', '#9E7794', '#B26D77', '#C56359', '#D8593B', '#EC4F1E', '#FF4500']  # Light to dark grey
        for idx, threshold in enumerate(thresholds):
            if value <= 0.0:
                return '#6495ED'
            if value <= threshold:
                return colors[idx]
        return colors[-1]  # Darkest color for anything above the highest threshold

    for row in range(num_rows):
        for i in range(num_circles):
            y_position = 0.3 - (row * 0.3)
            count = df.iloc[row, i]
            color = get_grey_scale_color(count)
            
            if row == 0:
                color = get_red_scale_color(count)
                #color = 'tomato'
                alpha = 1
            else:
                color = get_grey_scale_color(count)

            circle = plt.Circle((i * 0.3, y_position), circle_radius, color=color, fill=True)
            ax.add_artist(circle)

            for j in range(i + 1):
                angle = (j / (i + 1)) * 2 * np.pi
                x_end = (i * 0.3) + np.cos(angle) * line_length
                y_end = y_position + np.sin(angle) * line_length
                ax.plot([i * 0.3, x_end], [y_position, y_end], color=color)

    Gini = gini(G)
    IQ = (inequity(G))
    ei = EI(G)

    #print(Gini, IQ, ei)

    angle = 10 * IQ
    arc = Rectangle((0.3 * num_circles + 0.15, 0.4), 0.035, -0.5, color='#8BB0F2')
    ax.add_patch(arc)
    arc = Rectangle((0.3 * num_circles + 0.15, 0.15), 0.035, 0.25*IQ, color='#FFD700')
    ax.add_patch(arc)
    arc = Rectangle((0.3 * num_circles + 0.25, 0.4), 0.035, -0.5, color='#8BB0F2')
    ax.add_patch(arc)
    arc = Rectangle((0.3 * num_circles + 0.25, 0.15), 0.035, 0.25*ei, color='#FFD700')
    ax.add_patch(arc)
    arc = Rectangle((0.3 * num_circles + 0.05, 0.4), 0.035, -0.5, color='#8BB0F2')
    ax.add_patch(arc)
    arc = Rectangle((0.3 * num_circles + 0.05, 0.15), 0.035, 0.25*Gini, color='#FFD700')
    ax.add_patch(arc)
    arc = Rectangle((0.3 * num_circles + 0.05, 0.15), 0.035, -0.25*Gini, color='#FFD700')
    ax.add_patch(arc)
    ax.scatter([0.3 * num_circles + 0.07], [0.15], marker='_', color='#757575')
    ax.scatter([0.3 * num_circles + 0.17], [0.15], marker='_', color='#757575')
    ax.scatter([0.3 * num_circles + 0.265], [0.15], marker='_', color='#757575')

    ax.set_xlim(-0.1, num_circles * 0.3 + 0.3)
    ax.set_ylim(-0.2, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    if fig:
        plt.show()
        fig.savefig("network_diagram.svg", format='svg')

def read_network_nx(G):
    buckets1 = [0] * 10
    buckets2 = [0] * 10

    for n in G.nodes():
        count = G.degree(n)
        bucket_index = min(count, 10) - 1
        
        if G.nodes[n]['m'] == 0:
            buckets1[bucket_index] += count
        else:
            buckets2[bucket_index] += count



    df1 = pd.DataFrame([buckets1], columns=[f"{i+1}" for i in range(10)])
    df2 = pd.DataFrame([buckets2], columns=[f"{i+1}" for i in range(10)])

    row_sums = df1.sum(axis=1) + df2.sum(axis=1)
    # Divide each cell by the row total to get the relative shares
    df1 = df1.div(row_sums, axis=0)
    df2 = df2.div(row_sums, axis=0)
    
    max1 = df1.max(axis=1)
    max2 = df2.max(axis=1)

    maxx = max([max1[0], max2[0]])

    df1 = df1.div(maxx, axis=0)
    df2 = df2.div(maxx, axis=0)

    df = pd.concat([df2, df1], ignore_index=True)

    return G, df

# Example usage:
#plot_network(data,G)

# G = nx.karate_club_graph()

# for n in G.nodes():
#     if np.random.random() < 0.3:
#         G.nodes[n]['m'] = 0
#     else:
#         G.nodes[n]['m'] = 1

# print(gini(G))
# print(EI(G))
# print(inequity(G))

# write_csv(G)
# G = parse_csv('network.csv')

# print(gini(G))
# print(EI(G))
# print(inequity(G))

# with open('02_Inequality/data/raw/inequality_samplenetworks/json/N-200_m-2_f-0.3_h-0.2_tc-0.0_lfm-l-homophily_lfm-g-homophily_r-0.json') as file:
#     JSON = json.load(file)
#     G = nx.node_link_graph(JSON)

#     print(gini(G))
#     print(EI(G))
#     print(inequity(G))