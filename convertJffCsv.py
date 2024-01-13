import xml.etree.ElementTree as ET  # Importing the ElementTree module for XML parsing.
import pandas as pd  # Importing the pandas library for data manipulation and analysis.

def jff_to_csv(jff_filename, csv_filename):
    """
    Converts a JFLAP file (with a .jff extension) to a CSV format.

    This function first parses the JFLAP XML file to extract states and transitions. 
    The state information is stored in a dictionary, and transitions are stored in a list. 
    It then processes these details into a format suitable for a pandas DataFrame. 
    The DataFrame is saved to a CSV file, with the specified filename and semicolon as the separator.

    Args:
        jff_filename (str): The path to the JFLAP file.
        csv_filename (str): The path where the CSV file will be saved.

    Returns:
        None: The function does not return a value but saves the output in a CSV file.
    """
    # Parse the XML file and get the root element.
    tree = ET.parse(jff_filename)
    root = tree.getroot()

    # Initialize a dictionary for states and a list for transitions.
    states = {}
    transitions = []
    symbols = set()  # A set to store unique symbols.

    # Extract state information.
    for state in root.findall('.//state'):
        state_id = state.get('id')  # Get the state's ID.
        state_name = state.get('name')  # Get the state's name.
        # Determine if the state is initial (1) or not (0).
        is_initial = 1 if state.find('initial') is not None else 0
        # Determine if the state is final (1) or not (0).
        is_final = 1 if state.find('final') is not None else 0
        # Store the state information in the states dictionary.
        states[state_id] = {'name': state_name, 'is_initial': is_initial, 'is_final': is_final}

    # Extract transition information.
    for trans in root.findall('.//transition'):
        # Get the IDs of the from and to states.
        from_state_id = trans.find('from').text
        to_state_id = trans.find('to').text
        # Get the symbol read during the transition (default to empty if not found).
        read_symbol = trans.findtext('read', default='')

        # Get the names of the from and to states using their IDs.
        from_state = states[from_state_id]['name']
        to_state = states[to_state_id]['name']
        # Append the transition information to the transitions list.
        transitions.append((from_state, read_symbol, to_state))
        # Add the symbol to the set of symbols.
        symbols.add(read_symbol)

    # Prepare a list for DataFrame data.
    rows = []
    for state_info in states.values():
        # Initialize a row with all symbols set to empty.
        row = {symbol: '' for symbol in symbols}
        # Update the row with state information.
        row.update({'etat': state_info['name'], 'EI': state_info['is_initial'], 'EF': state_info['is_final']})
        rows.append(row)

    # Process transitions to update the rows.
    for from_state, read_symbol, to_state in transitions:
        for row in rows:
            if row['etat'] == from_state:
                # Append the to_state to the appropriate symbol column.
                if row[read_symbol] != '':
                    row[read_symbol] += ','
                row[read_symbol] = row[read_symbol] if row[read_symbol] != '' else to_state

    # Create a DataFrame from the rows.
    df = pd.DataFrame(rows)

    # Reorder the columns in the DataFrame.
    columns_order = ['etat'] + sorted(symbols) + ['EI', 'EF']
    df = df[columns_order]

    # Save the DataFrame to a CSV file.
    df.to_csv(csv_filename, index=False, sep=';')
