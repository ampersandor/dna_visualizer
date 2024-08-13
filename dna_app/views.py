# dna_app/views.py
from django.http import HttpResponse
from django.shortcuts import render
from .forms import DNAForm

import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO



def initialize_graph():
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 10)
    graph = nx.DiGraph()
    return graph

def add_seq(graph, seq):
    node_from = graph.number_of_nodes()
    node_to = node_from + len(seq) - 1
    connection_between_seq = [(i, i+1) for i in range(node_from, node_to)]
    graph.add_edges_from(connection_between_seq)
    return connection_between_seq


def is_complement(d1, d2):
    complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return d1 == complement_map.get(d2)

def get_binding_pairs(dna1, dna2):
    return [(idx, idx+len(dna1)) for idx, (d1, d2) in enumerate(zip(dna1, dna2)) if is_complement(d1, d2)]

def generate_pos(dna1, dna2):
    y_1 = 6
    y_2 = 5
    dna1_pos_dict = {x: (x+1, y_1) for x in range(len(dna1))}
    dna2_pos_dict = {x + len(dna1): (x+1, y_2) for x in range(len(dna2))}
    dna1_pos_dict.update(dna2_pos_dict)
    return dna1_pos_dict


def color_G_C_binding(G, node_position, binding_pairs, dna1, dna2):
    #TODO
    g_c_binding_nodes = []
    for i, j in binding_pairs:
        if {dna1[i], dna2[j-len(dna1)]} == {"G", "C"}:
            g_c_binding_nodes.append(i)
            g_c_binding_nodes.append(j)
    nx.draw_networkx_nodes(G, node_position, nodelist=g_c_binding_nodes, node_color='#454B1B', node_size=100)


def label_nodes(dna1, dna2):
    labels = {i: dna1[i] for i in range(len(dna1))}
    for j in range(len(dna2)):
        labels[j+len(dna1)] = fr"${dna2[j]}$"
    return labels

def draw(graph, node_position, red_edges, black_edges, labels):
    nx.draw_networkx_nodes(graph, node_position, node_color="tab:blue", node_size = 100)
    nx.draw_networkx_edges(graph, node_position, edgelist=red_edges, edge_color='r', arrows=False)
    nx.draw_networkx_edges(graph, node_position, edgelist=black_edges, arrows=False)
    nx.draw_networkx_labels(graph, node_position, labels, font_size=9, font_color="whitesmoke")


def show():
    plt.tight_layout()
    #plt.show()
    plt.savefig('myplot.png')


def plot_dna(request):
    # Extract DNA sequences from query parameters
    dna1 = request.GET.get('dna1')
    dna2 = request.GET.get('dna2')

    # Validate parameters
    if not dna1 or not dna2:
        return HttpResponseBadRequest("Both 'dna1' and 'dna2' query parameters are required.")

    G = initialize_graph()
    add_seq(G, dna1)
    add_seq(G, dna2)

    red_edges = get_binding_pairs(dna1, dna2)
    black_edges = [edge for edge in G.edges() if edge not in red_edges]

    node_position = generate_pos(dna1, dna2)
    labels = label_nodes(dna1, dna2)

    draw(G, node_position, red_edges, black_edges, labels)
    color_G_C_binding(G, node_position, red_edges, dna1, dna2)

    # Save plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')




def dna_input(request):
    form = DNAForm()
    return render(request, 'dna_app/dna_form.html', {'form': form})
