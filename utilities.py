import pandas as pd
import numpy as np

#modifier init_graph et init_statestypes par rapport au fichier test.csv
def init_graph(file) -> tuple:
    try:
        automate = pd.read_csv(file, sep=';')
        # Add a check for the expected number of columns
        if automate.shape[1] < 3:  # At least one state, one transition, EI, and EF
            raise ValueError("CSV file format is incorrect. Missing columns.")

        state_names = automate['etat'].tolist()
        transitions = automate.iloc[:, 1:-2]

        graph_to_list = []
        for i in range(len(transitions)):
            row = []
            for item in transitions.iloc[i].values:
                if item == '-':
                    row.append(['-'])
                else:
                    # Split by comma for multiple transitions
                    row.append(item.split(','))
            graph_to_list.append(row)

        return graph_to_list, state_names
    except FileNotFoundError:
        print(f"File {file} not found.")
        return [], []
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []



def init_statestypes(file)->list:
    """This function gets the types of the
    states (initial or final).

    Args:
        file (csv file): file that contains the matrix

    Returns:
        list: list of the states's types
    # """
    automate = pd.read_csv(file, sep=';')
    dimension: tuple=automate.shape
    states = automate.iloc[0 :dimension[0],dimension[1]-2 : dimension[1]]
    states_to_list=[states.loc[:,i].values.tolist() for i in ['EI', 'EF']]
    return states_to_list

def transitions(file)->list:
    automate=pd.read_csv(file,sep=';')
    return list(automate.columns)[1:automate.shape[1]-2]
