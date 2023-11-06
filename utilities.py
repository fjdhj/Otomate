import pandas as pd
import numpy as np

def init_graph(file)->list:
    """This function enable us to generate 
    matrix that contains the events and links from
    the CSV File.

    Args:
        file (_type_): _description_

    Returns:
        list: _description_
    # """
    automate = pd.read_csv(file, sep=';')
    dimension: tuple=automate.shape
    print(dimension)
    print(automate[automate[:] == 'q1,q3'])
    graph = automate.iloc[0 :dimension[0],0 : dimension[1]-2]
    graph_to_list=[graph.loc[i,:].values.tolist() for i in range(dimension[0])]
    return graph_to_list

def init_statestypes(file)->list:
    """This function gets the types of 
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
    print(states_to_list)
    return states_to_list

#init_graph('Sample/default.csv')
init_statestypes('Sample/default.csv')
        