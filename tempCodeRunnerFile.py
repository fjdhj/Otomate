    def edit_csv(self, filename):
        # Create a DataFrame to hold the CSV data
        csv_data = {
            'etat': self.all_states,
            'EI': self.initial_states,
            'EF': self.final_states
        }

        # Process transitions for each symbol
        for symbol_index, symbol in enumerate(self.transitions):
            csv_data[symbol] = []
            for state_index in range(len(self.all_states)):
                # Extract the transition state for this symbol
                transition_state = self.matrix[state_index][symbol_index + 1]

                # If the transition state is NaN, convert it to the string 'nan'
                if pd.isna(transition_state):
                    transition_str = ''
                else:
                    transition_str = transition_state

                csv_data[symbol].append(transition_str)

        # Convert the dictionary to a pandas DataFrame
        df = pd.DataFrame(csv_data)

        # Reorder the DataFrame columns to match the desired format
        column_order = ['etat'] + self.transitions + ['EI', 'EF']
        df = df[column_order]

        # Write to CSV using pandas, with the header
        df.to_csv(f"{filename}.csv", index=False, header=True, sep=';')
    