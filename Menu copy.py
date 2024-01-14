# Imports
from automate import automate
from convertCsvPng import draw_and_save_automaton
from convertJffCsv import jff_to_csv
import datetime
import os
import webbrowser


def enter_slot_number():
    """
    Function that requests a valid slot number from the user.
    Checks for valid arguments.
    
    Args: None

    Returns:
        slot : int (error = -1) 
    """
    while True:
        try:
            # Check if the chosen slot is between 1 and 10 inclusive
            slot = int(input("Enter the slot number (1-10) : "))
            if 1 <= slot <= 10:
                return slot  # Return the valid slot
            else:
                print("Please enter a number between 1 and 10.\n")
        except ValueError:
            # If a ValueError is detected, it means the user entered something other than an integer
            # Then, return an error value
            print("Please enter a valid integer number.\n")
            return -1


def modify_automaton(current_auto: automate):
    """
    Procedure for modifying an automaton.
    Asks the user what they want to modify, then applies the modification.
    Sub-menu of the main menu, which can be accessed with the last option.
    
    Args:
        current_auto : automate
    
    Returns: None
    """
    
    while current_auto.verify_states():
        # Display the modification menu
        print("\nAutomaton Modification Menu:")
        print("1. Add a state")
        print("2. Delete a state")
        print("3. Add a transition")
        print("4. Delete a transition")
        print("5. Add a link")
        print("6. Delete a link")
        print("7. Modify initial states")
        print("8. Modify final states")
        print("9. Return to main menu\n")
        modification_choice = input("Choose an action: ")

        if modification_choice == "1":
            # Apply the method to create a state of Automaton
            state_name = str(input("Enter the name of the new state: "))
            current_auto.create_state(state_name)
            
        elif modification_choice == "2":
            # Apply the method to delete a state of Automaton
            state_name = str(input("Enter the name of the state to delete: "))
            current_auto.delete_state(state_name)
            
        elif modification_choice == "3":
            # Apply the method to create a transition of Automaton
            transition_name = str(input("Enter the name of the new transition: "))
            current_auto.create_transition(transition_name)
            
        elif modification_choice == "4":
            # Apply the method to delete a transition of Automaton
            transition_name = str(input("Enter the name of the transition to delete: "))
            current_auto.delete_transition(transition_name)
            
        elif modification_choice == "5":
            # Request the start state and create it if needed
            initial_state_name = str(input("Enter the name of the start state: "))
            if not (initial_state_name in current_auto.all_states):
                current_auto.create_state(initial_state_name)
            
            # Request the end state and create it if needed
            final_state_name = str(input("Enter the name of the end state: "))
            if not (final_state_name in current_auto.all_states):
                current_auto.create_state(final_state_name)
            
            # Request the used transition and create it if needed
            transition_name = str(input("Enter the name of the transition: "))
            if not (transition_name in current_auto.transitions):
                current_auto.create_transition(transition_name)
            
            # Add the link based on previous inputs
            current_auto.add_transition(initial_state_name, transition_name, final_state_name)
            
        elif modification_choice == "6":
            # Request the start state and check if it exists
            initial_state_name = str(input("Enter the name of the start state: "))
            while not (initial_state_name in current_auto.all_states):
                print("This state does not exist")
                initial_state_name = str(input("Enter the name of the start state: "))
                
            # Request the end state and check if it exists
            final_state_name = str(input("Enter the name of the end state: "))
            while not (final_state_name in current_auto.all_states):
                print("This state does not exist")
                final_state_name = str(input("Enter the name of the end state: "))

            # Request the transition and check if it exists
            transition_name = str(input("Enter the name of the transition: "))
            while not (transition_name in current_auto.transitions):
                print("This transition does not exist")
                transition_name = str(input("Enter the name of the transition: "))
            
            # Delete the link
            current_auto.remove_transition(initial_state_name, transition_name, final_state_name)

        elif modification_choice == "7":
            if(len(current_auto.all_states) == 0):
                print("The automaton is empty, back to the menu\n")
            else:
                # Display initial states and allow modification
                print("Below is the list of initial states\n")
                for i in range(len(current_auto.initial_states)):
                    if current_auto.initial_states[i] == 1:
                        print(current_auto.all_states[i])
                # User chooses a state to modify its initial status
                state = input("Choose a state\n")
                while((not state in current_auto.all_states) and state != "cancel"):
                    state = input("The state doesn't exists, choose a state or enter 'cancel'\n")
                if(state != "cancel"):
                    index_state = current_auto.all_states.index(state)
                    if current_auto.initial_states[index_state] == 1:
                        if input("This state is currently initial, make it non-initial? y/n\n") == "y":
                            current_auto.demake_initial(state)
                    else:
                        if input("This state is currently non-initial, make it initial? y/n\n") == "y":
                            current_auto.make_initial(state)
                else:
                    print("Back to the menu \n")

        elif modification_choice == "8":
            if(len(current_auto.all_states) == 0):
                print("The automaton is empty, back to the menu\n")
            else:
                # Display final states and allow the user to modify them
                print("Below is the list of final states\n")
                for i in range(len(current_auto.final_states)):
                    if current_auto.final_states[i] == 1:
                        print(current_auto.all_states[i])
                # User chooses a state to modify its final status
                state = input("Choose a state\n")
                while(not state in current_auto.all_states):
                    state = input("Choose a state\n")
                index_state = current_auto.all_states.index(state)
                if current_auto.final_states[index_state] == 1:
                    if input("This state is currently final, make it non-final? y/n\n") == "y":
                        current_auto.demake_final(state)
                else:
                    if input("This state is currently non-final, make it final? y/n\n") == "y":
                        current_auto.make_final(state)

        elif modification_choice == "9":
            break
        else:
            print("Invalid choice. Please try again.\n")

def display_manual():
    """
    Display the user manual for the Automata Management System.
    
    Args: None
    
    Returns: None
    """
    manual = """
    ############################## User Manual ##############################

    Welcome to the Automata Management System. Below is a guide to using each feature of the system.

    1. Import Automaton:
       - Import an automaton from a file.
       - Input: CSV file name.
       - Output: Automaton loaded into an available slot.
       - Example: Input "automaton.csv" to import.

    2. Export Automaton:
       - Export an automaton to a file.
       - Input: Slot number and export file name.
       - Output: Automaton from the specified slot exported to the file.
       - Example: File name "export.csv" to export.

    3. Create Automaton:
       - Create a new automaton.
       - Input: Automaton details (states, transitions).
       - Output: New automaton stored in a slot.
       - Example: Provide state and transition details to create.

    4. Modify Automaton:
       - Modify an existing automaton.
       - Input: Slot number and modification details.
       - Output: Updated automaton in the slot.
       - Example: Input slot "3" to modify Automaton in Slot 3.

    5. Delete Automaton:
       - Delete an automaton from a slot.
       - Input: Slot number.
       - Output: Automaton in the slot is deleted.
       - Example: Input slot "4" to delete Automaton in Slot 4.

    6. Process a Word:
       - Check if a word is accepted by an automaton.
       - Input: Slot number and word.
       - Output: Result of word processing.
       - Example: Input slot "1" and word "abc" to test.

    7. Complete Automaton:
       - Check if an automaton is complete and complete it if needed.
       - Input: Slot number.
       - Output: Completeness status and option to complete.
       - Example: Input slot "5" to check and complete Automaton in Slot 5.

    8. Deterministic Automaton:
       - Check and convert an automaton to a deterministic form.
       - Input: Slot number.
       - Output: Information on whether the automaton is deterministic; option to convert it if not.
       - Example: Input slot "6" to check and convert Automaton in Slot 6 if necessary.

    9. Mirror Automaton:
       - Create a mirror version of the automaton.
       - Input: Slot number.
       - Output: Mirrored automaton in the same slot.
       - Example: Input slot "7" to mirror Automaton in Slot 7.

    10. Complement:
        - Generate the complement of an automaton.
        - Input: Slot number.
        - Output: Complement automaton in the same slot.
        - Example: Input slot "8" to complement Automaton in Slot 8.

    11. Product:
        - Create a product of two automata.
        - Input: Slot numbers of the two automata.
        - Output: Product automaton stored in a new slot.
        - Example: Input slots "2" and "3" to create a product of Automata in Slots 2 and 3.

    12. Concatenation:
        - Concatenate two automata.
        - Input: Slot numbers of the two automata.
        - Output: Concatenated automaton stored in a new slot.
        - Example: Input slots "4" and "5" to concatenate Automata in Slots 4 and 5.

    13. Extract Regular Expressions:
        - Extract regular expressions from an automaton.
        - Input: Slot number.
        - Output: Regular expressions corresponding to the automaton.
        - Example: Input slot "9" to extract expressions from Automaton in Slot 9.

    14. Find Language:
        - Determine the language of an automaton.
        - Input: Slot number.
        - Output: Description of the language recognized by the automaton.
        - Example: Input slot "10" to find the language of Automaton in Slot 10.

    15. Equivalence between 2 Automata:
        - Check the equivalence of two automata.
        - Input: Slot numbers of the two automata.
        - Output: Result of equivalence check.
        - Example: Input slots "1" and "2" to check equivalence between Automata in Slots 1 and 2.

    16. Trim Automaton:
        - Trim an automaton to remove unnecessary states.
        - Input: Slot number.
        - Output: Trimmed automaton in the same slot.
        - Example: Input slot "11" to trim Automaton in Slot 11.

    17. Minimize Automaton:
        - Minimize an automaton.
        - Input: Slot number.
        - Output: Minimized automaton in the same slot.
        - Example: Input slot "12" to minimize Automaton in Slot 12.

    18. Visualize Automaton:
        - Visualize and export the image of an automaton.
        - Input: Slot number.
        - Output: Visualization of the automaton and export as an image file.
        - Example: Input slot "13" to visualize and export Automaton in Slot 13.

    19. Convert .JFF to .CSV:
        - Convert a .JFF file to a .CSV file format.
        - Input: .JFF file name and .CSV file name.
        - Output: Converted .CSV file.
        - Example: Input "automaton.jff" and "automaton.csv" for conversion.

    20. Manual:
        - Displays this user manual.

    21. Exit Program:
        - Use this option to exit the program. Ensure to export any automata you wish to save.

    For more information or issues, refer to the system documentation or contact support.

    ############################################################################
    """
    print(manual)

def print_timestamp():
    """
    Formats the current time.
    
    Args: None

    Returns:
        formatted_time : string
    """
    
    # Retrieve the current time
    current_time = datetime.datetime.now()
    # Format the date
    formatted_time = current_time.strftime("%Y-%m-%d %H_%M_%S")
    # Return the formatted time
    return formatted_time

##########################################################################################
################################## Main Menu #############################################
##########################################################################################

# Instantiate the list of automata being processed
slots: list = [None] * 10

while True:
    
    # Temporary automaton variables instantiated to None
    automaton = None
    automaton1 = None
    automaton2 = None
    next_loop = 0
    
    # Display the contents of the slots
    i=0
    for auto in slots:
        #We check if the automaton is instantaneous or not in the slot
        if auto is not None:
            print("Slot ",i+1," : ", auto.name)
        else :
            print("Slot ",i+1," : None")
        i+=1
    print ("\n")

    # Check for the next empty slot (None if full)
    empty_slot = next((i for i, automate in enumerate(slots) if automate is None), None)
    
    ### SLOT MANAGEMENT ################################################################

    while empty_slot is None:
        # If no slot is available, ask the user to delete or export an automaton from a slot
        print("No available slots. Please delete one or export an automaton.")
        print("1. Delete an automaton\n2. Export an automaton\n")
        
        choice = input("Choose an action : ")
        print("\n")
        
        if choice == "1":
            slot = enter_slot_number()
            # If there's no error...
            if slot != -1: 
                # ... Delete the automaton corresponding to the slot
                slots[slot - 1] = None
                print("Deletion completed.\n\n")
                # next_loop allows returning to the beginning of the menu later
                next_loop = 1
                
        elif choice == "2":
            slot = enter_slot_number()
            # Apply the same method as in the main menu
            if slot != -1 and slots[slot-1] is not None:
                automaton: automate = slots[slot - 1]
                file_name = str(input("Type the file name to export automaton: "))
                if file_name.endswith(".csv"):
                    file_name = file_name.rstrip(".csv")
                path = os.path.dirname(file_name) + "/"
                basename = os.path.basename(file_name)
                if not os.path.exists(path):
                    print(f"The path '{file_name}' does not exist.\n")
                else:
                    automaton.edit_csv(basename, automaton.matrix, automaton.final_states)
                    print("Processing completed.\n\n")      
            else:
                print("Invalid slot. Please try again.\n")
            
        # Recalculate if a slot has been freed
        empty_slot = next((i for i, automate in enumerate(slots) if automate is None), None)
    
    # Exit the current occurrence if a slot has been freed
    if next_loop == 1:
        continue
            
    ### MAIN MENU ########################################################################
    
    print("\nMain Menu:\n")
    print("1. Import automaton")
    print("2. Export automaton")
    print("3. Create automaton")
    print("4. Modify automaton")
    print("5. Delete FSA")
    print("6. Process a word")
    print("7. Complete automaton")
    print("8. Deterministic automaton")
    print("9. Mirror")
    print("10. Complement")
    print("11. Product")
    print("12. Concatenation")
    print("13. Extract regular expressions")
    print("14. Find language")
    print("15. Equivalence between 2 automata")
    print("16. Trim automaton")
    print("17. Minimize automaton")
    print("18. Visualize an automaton")
    print("19. Convert .JFF to .CSV")
    print("20. Manual")
    print("21. Quit the program\n")
    choice = input("Choose an action : ")
    print("\n")

    ### IMPORTATION ##############################################################
    
    if choice == "1":
        if empty_slot is not None:
            # Ask for the file path to save the automaton
            file_name = str(input("Type the file name to import automaton: "))
            
            # Add the .csv extension if missing
            if not file_name.endswith(".csv"):
                file_name += ".csv"
            
            # If the path does not exist, display an error message
            if not os.path.exists(file_name):
                print(f"The file '{file_name}' does not exist.\n")
            
            # Otherwise, create the automaton in the next empty slot
            else:
                automaton = automate(file_name) 
                if(automaton.verify_states()):
                    slots[empty_slot] = automaton
                    print(slots)
                    print("Automaton saved in slot: ", empty_slot + 1, "\n\n")
                
        else:
            print("No available slots to create a new automaton.\n")  
    
    ### EXPORTATION ##############################################################
    
    elif choice == "2":
        
        slot = enter_slot_number()
        
        # Check if the slot is valid and not empty
        if slot != -1 and slots[slot - 1] is not None:
            automaton: automate = slots[slot - 1]
            
            # Ask for the file name to export the automaton
            file_name = str(input("Type the file name to export automaton: "))
            
            # Add the .csv extension if needed
            if file_name.endswith(".csv"):
                file_name = file_name.rstrip(".csv")
            
            # Check if the path exists and display an error message if necessary
            path = os.path.dirname(file_name) + "/"
            basename = os.path.basename(file_name)
            if not os.path.exists(path):
                print(f"The path '{file_name}' does not exist.\n")
            # If all is well, edit the file
            else:
                automaton.edit_csv(file_name, automaton.matrix, automaton.final_states)
                print("Processing completed.\n\n")
                
        else:
            print("Invalid slot. Please try again.\n")

    ### CREATION #################################################################
    
    elif choice == "3":
        
        if empty_slot is not None:
            
            # Ask for the file name where to create the automaton
            file_name = str(input("Type the file name to create automaton: "))
            
            # Add the .csv extension if needed
            if not file_name.endswith(".csv"):
                file_name += ".csv"
                
            # Check if the path exists
            dir = os.path.dirname(file_name)
            if not os.path.exists(dir) and dir != "":
                print(f"The path '{file_name}' does not exist.\n")
            # If all is well, create the file and the automaton in the next empty slot
            else:
                slots[empty_slot] = automate(file_name)
                print(slots)
                print("Processing completed.\n\n")
                
        else:
            print("No available slots to create a new automaton.\n")   

    ### MODIFICATION ############################################################
    
    elif choice == "4":
        
        slot = enter_slot_number()
        if slot != -1:
            
            # Retrieve the corresponding automaton
            automaton = slots[slot - 1]
            
            # If the automaton exists, open the modification menu
            if automaton:
                modify_automaton(automaton)
                print("Processing completed.\n\n")
            
            else:
                print("No automaton in this slot.\n")
        
    ### DELETION #################################################################
    
    elif choice == "5":
        
        slot = enter_slot_number()
        if slot != -1:
            
            # Overwrite the automaton corresponding to the provided slot
            slots[slot - 1] = None
            print("Deletion completed.\n\n")

    ### PROCESS A WORD ###########################################################

    elif choice == "6":

        # Retrieve the slot and corresponding automaton
        slot = enter_slot_number()
        if slot != -1:
            automaton: automate = slots[slot - 1]

            # If the automaton exists... and is deterministic
            if automaton and automaton.is_deterministic():
                # ...Retrieve the word to check
                word = input("Enter a word to be recognized by the automaton: \n")

                # Check if the word is recognized, and display the result
                if automaton.recognize_wordAFD(word):
                    print("The word is recognized.\n")
                else:
                    print("The word is not recognized.\n")
            elif automaton and not automaton.is_deterministic():
                # Make it deterministic and recognize the word
                if input("The automaton is not deterministic, would you like to make it deterministic? [Y/N]\n") == "Y":
                    auto = automaton.AND_to_AFD()
                    print("Processing completed.\n\n")
                    word = input("Enter a word to be recognized by the automaton: \n")

                    # Check if the word is recognized, and display the result
                    if automaton.recognize_wordAFD(word):
                        print("The word is recognized.\n")
                    else:
                        print("The word is not recognized.\n")
            else:
                print("No automaton in the slot.\n")

    ### COMPLETE AUTOMATON #######################################################

    elif choice == "7":

        # Retrieve the slot and corresponding automaton
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]

            # If the automaton exists...
            if automaton:
                # ...check if it is complete. If so, display it and exit.
                if automaton.is_complete():
                    print("The automaton is complete.\n")

                else:
                    # If the automaton is not complete, offer to complete it.
                    if input("The automaton is not complete, would you like to complete it? [Y/N]\n") == "Y":
                        automaton.make_complete()
                        print("Processing completed.\n\n")

            else:
                print("No automaton in this slot.\n")

    ### DETERMINISTIC AUTOMATON ###################################################

    elif choice == "8":

        # Retrieve the slot and corresponding automaton
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]

            # If the automaton exists...
            if automaton:
                # ...check if it is deterministic. If so, exit.
                if automaton.is_deterministic():
                    print("The automaton is deterministic.\n")

                else:
                    # If it is not deterministic, offer to make it deterministic.
                    if input("The automaton is not deterministic, would you like to make it deterministic? [Y/N]\n") == "Y":
                        auto = automaton.AND_to_AFD()
                        print("Processing completed.\n\n")

            else:
                print("No automaton in this slot.\n")

    ### MIRROR AUTOMATON ##########################################################

    elif choice == "9":

        # Retrieve the automaton corresponding to the requested slot
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]

            # If the automaton exists, store its mirror
            if automaton:
                automaton.mirror()
                print("Processing completed.\n\n")

            else:
                print("No automaton in this slot.\n")

    ### COMPLEMENT AUTOMATON ######################################################

    elif choice == "10":

        # Retrieve the automaton corresponding to the requested slot
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]

            # If the automaton exists, store its complement
            if automaton:
                automaton.complement()
                print("Processing completed.\n\n")

            else:
                print("No automaton in this slot.\n")

    ### PRODUCT OF AUTOMATA #######################################################

    elif choice == "11":

        # Retrieve the slot and corresponding automaton
        slot = enter_slot_number()
        if slot != -1:
            automaton1 = slots[slot - 1]

            # Retrieve the slot for the second automaton
            slot = enter_slot_number()
            if slot != -1:
                automaton2 = slots[slot - 1]

        # If both automata exist, store their product in the next available slot
        if automaton1 and automaton2:
            next_empty_slot = next((i for i, automate in enumerate(slots) if automate is None), None)
            slots[next_empty_slot] = automaton1.product(automaton2)
            print("Automaton saved in slot: ", next_empty_slot + 1, "\n\n")
            print("Processing completed.\n\n")

        # Otherwise, display where there's an error
        else:
            if not automaton1:
                print("There is no automaton in the first slot.\n")
            elif not automaton2:
                print("There is no automaton in the second slot.\n")
            else:
                print("There was a problem.\n")

    ### CONCATENATION #############################################################

    elif choice == "12":

        # Retrieve the first automaton
        slot = enter_slot_number()
        if slot != -1:
            automaton1 = slots[slot - 1]

            # Retrieve the second automaton
            slot = enter_slot_number()
            if slot != -1:
                automaton2 = slots[slot - 1]

        # If both automata exist, concatenate them in the next available slot
        if automaton1 and automaton2:
            next_empty_slot = next((i for i, automate in enumerate(slots) if automate is None), None)
            automaton_concatenated = automaton1.concatenate(automaton2)
            slots[next_empty_slot] = automaton_concatenated
            print("Automaton saved in slot: ", next_empty_slot, "\n\n")
            automaton_concatenated.edit_csv("test", automaton_concatenated.matrix, automaton_concatenated.final_states)
            print("Processing completed.\n\n")

        else:
            print("At least one of the automata does not exist in the chosen slots.\n")

    ### EXTRACT REGULAR EXPRESSION ################################################

    elif choice == "13":
        slot = enter_slot_number()
        if slot != -1:
            automaton: automate = slots[slot - 1]
            if automaton:
                print("The regular expression of this automaton is :", automaton.get_regular_expression())
            else:
                print("No automaton in this slot.")

    ### DETERMINE LANGUAGE ########################################################

    elif choice == "14":
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]
            if automaton:
                print("The language of this automaton is: L = {%s}" % (automaton.get_regular_expression()))
            else:
                print("No automaton in this slot.")

    ### EQUIVALENCE BETWEEN TWO AUTOMATA ##########################################

    elif choice == "15":
        slot = enter_slot_number()
        if slot != -1 :
            automaton1 = slots[slot - 1]
            slot = enter_slot_number()
            if slot != -1 :
                automaton2 = slots[slot - 1]
        if automaton1 and automaton2:
            res = automaton1.isEquivalent(automaton2)

            if res:
                print("\nThe language of the two automatons is equivalent.\n")
            else:
                print("\nThe language of the two automata is not equivalent.\n")

        else:
            print("No automaton in one of the slots.")

    ### TRIM AUTOMATON ###########################################################

    elif choice == "16":
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]
            if automaton:
                print("You have chosen to trim the automaton\n")
                automaton = automaton.trim()
                print("Processing completed.\n\n")
            else:
                print("No automaton in this slot.")

    ### MINIMIZE AUTOMATON ########################################################

    elif choice == "17":
        slot = enter_slot_number()
        if slot != -1:
            automaton = slots[slot - 1]
            if automaton:
                print("You have chosen to minimize the automaton\n")
                automaton = automaton.minimize()
                print("Processing completed.\n\n")
            else:
                print("No automaton in this slot.")

    ### VISUALIZATION #############################################################

    elif choice == "18":
        slot = enter_slot_number()
        if slot != -1 :
            automaton = slots[slot - 1]
        else:
            automaton = None
        if automaton:
            # Ensure the output directory exists
            os.makedirs('output-png', exist_ok=True)

            # Define the CSV and image file paths
            csv_path = 'buffer.csv'  # Replace with your actual CSV file path
            timestamp = print_timestamp()
            image_filename = f'otomate_{timestamp}'

            automaton.edit_csv(csv_path[:-4], automaton.matrix, automaton.final_states)

            # Set the image path with a timestamp
            image_path = os.path.join('output-png', image_filename)

            # Process the CSV file and save the automaton image
            draw_and_save_automaton(csv_path, image_path)
            image_path_with_extension = image_path + '.png'

            # Open the saved image in a web browser
            webbrowser.open('file://' + os.path.realpath(image_path_with_extension))

            #Erase .dot file
            os.remove('output-png/' + (image_filename))
            os.remove(csv_path)


            print("Processing completed.\n\n")
        else:
            print("No automaton in this slot.\n")


    ### JFF TO CSV #################################################################

    elif choice == "19":
        # Request files to convert
        print("You want to convert a .jff file to a .csv file\n")
        jff_filename = input("Enter the name of the .jff file: ")
        csv_filename = input("Enter the name of the .csv file: ")

        # If the path does not exist, display an error message
        if not os.path.exists(jff_filename) and not os.path.exists(csv_filename):
            print(f"One of the files does not exist.\n")

        # Otherwise, apply the function
        else:
            jff_to_csv(jff_filename, csv_filename)

    ### MANUAL #####################################################################

    elif choice == "20":
        # Display the manual
        display_manual()

    ### EXIT PROGRAM ###############################################################

    elif choice == "21":
        # Ask the user if they have exported all automata they wish to save before exiting
        user_input = input("After exiting, your automata will be deleted from the slots.\nHave you exported all the automata you wanted to? (Y/N) \n")
        if user_input in ["Y", "YES", "Yes", "y", "yes"]:
            # If yes, exit
            print("Thank you and see you soon!")
            break

        # Otherwise, return to the main menu
        else:
            print("\nReturning to the main menu.\n")

    # Invalid choice case
    else:
        print("\nInvalid choice. Please try again.\n") 
