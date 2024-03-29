import pandas as pd
import numpy as np
import math
#modifier init_graph et init_statestypes par rapport au fichier test.csv
def init_graph(file)->list:
    """This function enable us to generate 
    matrix that contains the events and links from
    the CSV File.

    Args:
        file (csv file): _description_

    Returns:
        list: 2D arrays which contains automaton graph
    # """
    automate = pd.read_csv(file, sep=';')
    dimension: tuple=automate.shape
    graph = automate.iloc[0 :dimension[0],0 : dimension[1]-2]
    graph_to_list=[graph.loc[i,:].values.tolist() for i in range(dimension[0])]  
    graph_to_list_final = [["nan" if type(graph_to_list[i][j]) == float or graph_to_list[i][j] == np.nan else graph_to_list[i][j] for j in range(len(graph_to_list[i]))] for i in range(len(graph_to_list)) ]      
    return graph_to_list_final

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