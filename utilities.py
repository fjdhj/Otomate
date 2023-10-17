import pandas as pd


automate = pd.read_csv('Sample/default.csv', sep=';')
dimension=automate.shape
graphe = automate.iloc[1:dimension[0],1:dimension[1]-2]
print(graphe.head())
    