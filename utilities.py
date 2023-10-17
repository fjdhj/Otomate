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
    """
    automate = pd.read_csv(file, sep=';')
    dimension=automate.shape
    graph = automate.iloc[0:dimension[0],1:dimension[1]-2]
    graph_to_list=[graph.loc[i, :].values.flatten().tolist() for i in range(dimension[0])]
    return graph_to_list

init_graph('Sample/default.csv')
        