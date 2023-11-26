import os
import pandas as pd
from graphviz import Digraph

def csv_to_graphviz(csv_filename):
    # Read CSV using pandas
    df = pd.read_csv(csv_filename, delimiter=';')

    # Create a directed graph
    dot = Digraph(comment='Automaton')

    # Invisible nodes for initial state arrows
    for index, row in df.iterrows():
        if bool(row['EI']):  # If it's an initial state
            # Adjust the width and height to control arrow length
            dot.node(f'init_{row["etat"]}', '', shape='point', width='0.1', height='0.1')

    # Add nodes and edges based on DataFrame 'df'
    for index, row in df.iterrows():
        state_name = row['etat']
        is_initial = bool(row['EI'])
        is_final = bool(row['EF'])

        # Customize node attributes based on initial or final state
        node_shape = 'doublecircle' if is_final else 'circle'
        dot.node(state_name, state_name, shape=node_shape)

        # Add edge from invisible node to initial state with green color
        if is_initial:
            dot.edge(f'init_{state_name}', state_name, color='green')
# ...

        # Add edges for transitions
        for input_symbol in df.columns[1:-2]:  # Skip 'etat', 'EI', 'EF'
            if pd.notnull(row[input_symbol]) and row[input_symbol] != 'nan':
                targets = str(row[input_symbol]).split(',')
                for target in targets:
                    target = target.strip()  # Clean whitespace
                    if target and 'nan' not in target:
                        # Skip adding an edge if any part of the target contains 'nan'
                        dot.edge(state_name, target, label=input_symbol)

        # ...

    return dot

def draw_and_save_automaton(csv_filename, output_image_filename):
    dot = csv_to_graphviz(csv_filename)

    # Customize graph aesthetics
    dot.attr(rankdir='LR', size='16,10')  # Increase the size as needed
    dot.attr('node', shape='circle')
    dot.attr(dpi='300')  # Adjust DPI for higher resolution

    # Save the graph as an image
    dot.render(output_image_filename, view=False, format='png')


# Ensure the output directory exists
os.makedirs('output-png', exist_ok=True)

# Paths for the CSV and the image file
csv_path = 'Sample/default.csv'  # Replace with your actual CSV file path
image_path = os.path.join('output-png', 'otomate')

# Process the CSV file and save the automaton image
draw_and_save_automaton(csv_path, image_path)
