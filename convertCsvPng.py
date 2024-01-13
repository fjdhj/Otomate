import os
import pandas as pd
from graphviz import Digraph

def csv_to_graphviz(csv_filename):
    """
    Reads a CSV file to create a Graphviz directed graph representing an automaton.

    Args:
    csv_filename (str): The path to the CSV file containing automaton data.
    
    The CSV file is expected to have columns representing states ('etat'), 
    initial state indicator ('EI'), final state indicator ('EF'), and other columns 
    representing transition symbols. Each row represents a state and its transitions.

    Returns:
    Digraph: A directed graph (automaton) as represented in the CSV file.
    """

    # Read CSV using pandas with ';' as delimiter
    df = pd.read_csv(csv_filename, delimiter=';')

    # Initialize a directed graph with a comment
    dot = Digraph(comment='Automaton')

    # Create invisible nodes for initial states
    for index, row in df.iterrows():
        if row['EI'] == 1:  # Check if it's an initial state
            dot.node(f'init_{row["etat"]}', '', shape='point', width='0.1', height='0.1')

    # Iterate over rows to add nodes and edges to the graph
    for index, row in df.iterrows():
        state_name = row['etat']
        is_initial = row['EI'] == 1
        is_final = row['EF'] == 1

        # Set node shape based on whether it's a final state
        node_shape = 'doublecircle' if is_final else 'circle'
        dot.node(state_name, state_name, shape=node_shape)

        # Add an edge from the invisible initial node to the actual initial state
        if is_initial:
            dot.edge(f'init_{state_name}', state_name, color='green')

        # Add edges for transitions
        for input_symbol in df.columns[1:-2]:  # Exclude 'etat', 'EI', 'EF' columns
            if pd.notnull(row[input_symbol]) and row[input_symbol] != '':
                targets = str(row[input_symbol]).split(',')
                for target in targets:
                    target = target.strip()  # Remove any surrounding whitespace
                    if target:
                        dot.edge(state_name, target, label=input_symbol)

    return dot

def draw_and_save_automaton(csv_filename, output_image_filename):
    """
    Generates an automaton image from a CSV file and saves it.

    Args:
    csv_filename (str): The path to the CSV file containing automaton data.
    output_image_filename (str): The path (without extension) where the image will be saved.

    This function uses 'csv_to_graphviz' to create a graph and then saves it as a PNG image.
    """

    # Create the graph from the CSV file
    dot = csv_to_graphviz(csv_filename)

    # Set graph aesthetics (layout direction, size, node shape, and resolution)
    dot.attr(rankdir='LR', size='16,10')
    dot.attr('node', shape='circle')
    dot.attr(dpi='300')  # High resolution

    # Save the graph as a PNG image
    dot.render(output_image_filename, view=False, format='png')
