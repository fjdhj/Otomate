import xml.etree.ElementTree as ET
import pandas as pd

def jff_to_csv(jff_filename, csv_filename):
    tree = ET.parse(jff_filename)
    root = tree.getroot()

    # Dictionnaire pour les états et les transitions
    states = {}
    transitions = []
    symbols = set()

    # Extraction des informations d'état
    for state in root.findall('.//state'):
        state_id = state.get('id')
        state_name = state.get('name')
        is_initial = 1 if state.find('initial') is not None else 0
        is_final = 1 if state.find('final') is not None else 0
        states[state_id] = {'name': state_name, 'is_initial': is_initial, 'is_final': is_final}

    # Extraction des informations de transition
    for trans in root.findall('.//transition'):
        from_state_id = trans.find('from').text
        to_state_id = trans.find('to').text
        read_symbol = trans.findtext('read', default='nan')

        from_state = states[from_state_id]['name']
        to_state = states[to_state_id]['name']
        transitions.append((from_state, read_symbol, to_state))
        symbols.add(read_symbol)

    # Création d'une liste pour les données DataFrame
    rows = []
    for state_info in states.values():
        row = {symbol: 'nan' for symbol in symbols}
        row.update({'etat': state_info['name'], 'EI': state_info['is_initial'], 'EF': state_info['is_final']})
        rows.append(row)

    # Traitement des transitions
    for from_state, read_symbol, to_state in transitions:
        for row in rows:
            if row['etat'] == from_state:
                if row[read_symbol] != 'nan':
                    row[read_symbol] += ','
                row[read_symbol] = row[read_symbol] if row[read_symbol] != 'nan' else to_state

    # Création de DataFrame
    df = pd.DataFrame(rows)

    # Réordonner les colonnes
    columns_order = ['etat'] + sorted(symbols) + ['EI', 'EF']
    df = df[columns_order]

    # Sauvegarder le DataFrame en fichier CSV
    df.to_csv(csv_filename, index=False, sep=';')

# Exemple d'utilisation
jff_filename = 'test.jff'  # Remplacer par le chemin de votre fichier JFLAP
csv_filename = 'otomate5.csv'  # Remplacer par le chemin souhaité pour le fichier CSV
jff_to_csv(jff_filename, csv_filename)
