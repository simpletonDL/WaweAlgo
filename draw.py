import os

import networkx as nx
import matplotlib.pyplot as plt
from time import gmtime, strftime

SEND_COLOR = "red"
RETRIEVE_COLOR = "red"
DEFAULT_EDGE_COLOR = "black"
DEFAULT_NODE_COLOR = "blue"
DESIDE_COLOR = "green"


def save_image(g, pos, file_name):
    edges = g.edges()
    edge_color = [g[u][v]["color"] for u, v in edges]
    node_color = [g.nodes[u]['color'] for u in g.nodes()]
    nx.draw(g, pos=pos, with_labels=True, node_color=node_color, edge_color=edge_color,
            font_weight='bold', connectionstyle='arc3, rad = 0.1')
    print(file_name)
    plt.savefig(file_name)


def draw_states(n, operations):
    if not os.path.exists("results"):
        os.mkdir("results")

    time = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    work_dir = f"results/{time}"
    os.mkdir(work_dir)

    def gen_name(x):
        return f"{work_dir}/img{x}"

    g = nx.DiGraph()
    g.add_node(0, color=DEFAULT_NODE_COLOR)
    for i in range(n):
        g.add_node(i, color=DEFAULT_NODE_COLOR)
        # g.nodes[i]['color'] = "blue"
        g.add_edge(0, i, color=DEFAULT_EDGE_COLOR)
        g.add_edge(i, 0, color=DEFAULT_EDGE_COLOR)
    pos = nx.spring_layout(g)

    save_image(g, pos, gen_name("0"))
    for i, (op_type, v, to, _) in enumerate(operations):
        if op_type == 'send':
            g[v][to]['color'] = RETRIEVE_COLOR
            g.nodes[v]['color'] = DEFAULT_NODE_COLOR
        elif op_type == 'recv':
            if v != 0:
                g.nodes[v]['color'] = RETRIEVE_COLOR
            g[to][v]['color'] = DEFAULT_EDGE_COLOR
        if i == len(operations) - 1:
            g.nodes[0]['color'] = DESIDE_COLOR
        save_image(g, pos, gen_name(i+1))


# draw_states(6, [["send", 0, 2, 5], ["recv", 2, 0, 5], ["send", 2, 0, 5]])
