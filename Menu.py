from automate import automate
from convertCsvPng import draw_and_save_automaton
from convertJffCsv import jff_to_csv

import os
import webbrowser


def modifier_automate(actual_auto:automate):
    # Menu de modification d'automate
    while True:
        print("\nMenu de modification d'automate :")
        print("1. Rajouter un état")
        print("2. Supprimer un état")
        print("3. Ajouter une transition")
        print("4. Supprimer une transition")
        print("5. Ajouter une liaison")
        print("6. Supprimer une liaison")
        print("7. Modifier états initiaux")
        print("8. Modifier états finals")
        print("9. Revenir au menu principal\n")
        choix_modification = input("Choisissez une action : ")

        if choix_modification == "1":
            state_name = str(input("Entrez le nom du nouvel état"))
            actual_auto.create_state(state_name)
        elif choix_modification == "2":
            state_name = str(input("Entrez le nom de l'état à supprimer"))
            actual_auto.delete_state(state_name)
        elif choix_modification == "3":
            transition_name = str(input("Entrez le nom de la nouvelle transition"))
            actual_auto.create_transition(transition_name)
        elif choix_modification == "4":
            transition_name = str(input("Entrez le nom de la transition à supprimer"))
            actual_auto.delete_transition(transition_name)
        elif choix_modification == "5":
            initial_state_name = str(input("Entrez le nom de l'état de départ"))
            if not (initial_state_name in actual_auto.all_states):
                actual_auto.create_state(initial_state_name)
                
            final_state_name = str(input("Entrez le nom de l'état d'arrivée"))
            if not (initial_state_name in actual_auto.all_states):
                actual_auto.create_state(final_state_name)
                
            transition_name = str(input("Entrez le nom de la transition"))
            if not (transition_name in actual_auto.transitions):
                actual_auto.create_transition(transition_name)
                
            actual_auto.add_transition(initial_state_name, transition_name, final_state_name)
        elif choix_modification == "6":
            #FIXME NATHAN Supprimer liaison 
            pass
        elif choix_modification == "7":
            i_initial_state=actual_auto.initial_states.index(1)
            print(f"Voici l'état initial: {actual_auto.all_states[i_initial_state]}")
            new_initial_state=str(input(f"Choisissez un automate à rendre en état initial parmi ceux là:\n{actual_auto.all_states}"))
            state_in_states:bool=new_initial_state in actual_auto.all_states
            while not state_in_states:
                new_initial_state=str(input(f"Choisissez un automate à rendre en état initial parmi ceux là:\n{actual_auto.all_states}"))
            actual_auto.initial_states[i_initial_state]=0
            actual_auto.initial_states[actual_auto.all_states.index(new_initial_state)] = 1
            i_initial_state=actual_auto.initial_states.index(1)
            print(f"Voici le nouvel état initial: {actual_auto.all_states[i_initial_state]}")
        elif choix_modification == "8":
            i_final_states=[i for i in range(len(actual_auto)) if actual_auto[i]==1]
        elif choix_modification == "9":
            break
        else:
            print("Choix invalide. Veuillez réessayer.\n")

def display_manual():
    """
    Display the user manual for the Automata Management System.
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

    16. Prune Automaton:
        - Prune an automaton to remove unnecessary states.
        - Input: Slot number.
        - Output: Pruned automaton in the same slot.
        - Example: Input slot "11" to prune Automaton in Slot 11.

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


##########################################################################################
################################## Menu principal ########################################
##########################################################################################


# Instancie la liste des automates en traitement
slots = [None] * 10

while True:
    
    
    # Trouve le prochain slot vide (NONE si complet)
    slot_vide = next((i for i, automate in enumerate(slots) if automate is None), None)
    
    
    ### GESTION DES SLOTS ################################################################
    
    """
    while slot_vide == None:
        print ("Aucun slot de disponible. Veuillez en supprimer un ou l'exporter.")
        print("1. Supprimer un automate\n2. Exporter un automate\n")
        
        choix = input("Choisissez une action : \n1. Supprimer automate\n2. Exporter automate\n")
        
        if choix == "1":
            #supprimer_automate()
        elif choix == "2":
            #exporter_automate()
    """
            
            
    ### MENU #############################################################################
    
    print("\nMenu principal :\n")
    print("1. Importer automate")
    print("2. Exporter automate")
    print("3. Créer automate")
    print("4. Modifier automate")
    print("5. Supprimer AEF")
    print("6. Passer un mot")
    print("7. Automate complet")
    print("8. Automate déterministe")
    print("9. Miroir")
    print("10. Complément")
    print("11. Produit")
    print("12. Concaténation")
    print("13. Extraction des expressions régulières")
    print("14. Trouver langage")
    print("15. Equivalence entre 2 automates")
    print("16. Emonder automate")
    print("17. Rendre un automate minimal")
    print("18. Visualiser un automate")
    print("19. Convertir .JFF en .CSV")
    print("20. Manuel")
    print("21. Quitter le programme\n")
    choix = input("Choisissez une action : ")
    print("\n")


    ### IMPORTATION ##############################################################
    
    #FIXME NATHAN Si le paramètre entré ne correspond pas à un slot ça plante
    if choix == "1":
        if slot_vide is not None:
            file_name=str(input("Type the file name to import automaton:\n"))
            slots[slot_vide] = automate(file_name) 
            print(slots)
            print("Automate enregistré dans le slot : ",slot_vide,"\n\n")
        else:
            print("Aucun slot disponible pour créer un nouvel automate.\n")  
    
    ### EXPORTATION ##############################################################
        
    elif choix == "2":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        #is_deterministic:bool=str(input("Votre tableau est il un tableau que vous avez déterminiser [y/n]"))
        automaton :automate= slots[slot - 1]
        file_name=str(input("Type the file name to export automaton:\n"))
        automaton.edit_csv(file_name, automaton.matrix,automaton.final_states)
        print("Traitement effectué.\n\n")
            
    # ### CREATION #################################################################
     
    elif choix == "3":
        if slot_vide is not None:
            file_name=str(input("Type the file name to import automaton:\n"))
            slots[slot_vide] = automate(file_name)
            print(slots)
            print("Traitement effectué.\n\n")
        else:
            print("Aucun slot disponible pour créer un nouvel automate.\n")   
    
    # ### MODIFICATION ############################################################
            
    elif choix == "4":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            modifier_automate(automaton)
            print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
            
            
    # ### SUPPRESSION #############################################################
            
    elif choix == "5":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        slots[slot - 1] = None
        print("Surppression effectuée.\n\n")
        
        
    # ### PASSER UN MOT ###########################################################
        
    elif choix == "6":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        qu = input("Ecrivez un mot à reconnaitre pour l'automate: \n")
        automaton: automate = slots[slot - 1]
        if automaton:
            recognize=automaton.recognize_wordAFD(qu)
            if recognize:
                print("Le mot est reconnu")
            else:
                print("Le mot n'est pas reconnu")
        else:
            print("Aucun automate dans le slot")
            
            
    # ### AUTOMATE COMPLET #######################################################
            
    elif choix == "7":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            if(automaton.is_complete()):
                print("L'automate est complet.")
            else:
                if(input("L'automate n'est pas complet, voulez-vous le rendre complet ? [Y/N]\n") == "Y"):
                    automaton.make_complete()
                    print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
            
    
    # ### AUTOMATE DETERMINISTE #################################################
            
    elif choix == "8":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            if(automaton.is_deterministic()):
                print("L'automate est déterministe.")
            else:
                if(input("L'automate n'est pas déterministe, voulez-vous le rendre déterministe ? [Y/N]\n") == "Y"):
                    auto=automaton.AND_to_AFD()
                    print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
            
            
    # ### AUTOMATE MIROIR ######################################################
            
    elif choix == "9":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            automaton.mirror()
            print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
            
        
    # ### AUTOMATE COMPLEMENTAIRE #############################################
            
    elif choix == "10":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            automaton.complement()
            print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
    
    
    # ### PRODUIT D'AUTOMATES #################################################
            
    elif choix == "11":
        slot = int(input("Entrez le numéro du slot (1-10) du premier automate : "))
        automaton1 = slots[slot - 1]
        slot = int(input("Entrez le numéro du slot (1-10) du second automate : "))
        automaton2 = slots[slot - 1]
        if automaton1 & automaton2:
            automaton1.product(automaton2)
            print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
            
            
    # ### CONCATENATION ######################################################
            
    # elif choix == "12":
    #     slot = int(input("Entrez le numéro du slot (1-10) du premier automate : "))
    #     automate1 = slots_automates[slot - 1]
    #     slot = int(input("Entrez le numéro du slot (1-10) du second automate : "))
    #     automate2 = slots_automates[slot - 1]
    #     if automate1 & automate2:
    #         #res = concatenation(automate1,automate2)
    #         #if res != None:
    #             #slot[slot_vide] = res
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### EXTRAIRE EXPRESSION ################################################
            
    # elif choix == "13":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #extraire_expression(automate, mot)
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### DETERMINER LANGAGE ################################################
            
    # elif choix == "14":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #langage_automate(automate)
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### LANGAGES EQUIVALENTS ##############################################
            
    # elif choix == "15":
    #     slot = int(input("Entrez le numéro du slot (1-10) du premier automate : "))
    #     automate1 = slots_automates[slot - 1]
    #     slot = int(input("Entrez le numéro du slot (1-10) du second automate : "))
    #     automate2 = slots_automates[slot - 1]
    #     if automate1 & automate2:
    #         #res = equivalence(automate1,automate2)
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### EMONDER AUTOMATE ##################################################
            
    # elif choix == "16":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #res = emonder(automate)
    #         #if res != None:
    #             #slot[slot_vide] = res
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### RENDRE MINIMAL ###################################################
            
    # elif choix == "17":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #res = minimal(automate)
    #         #if res != None:
    #             #slot[slot_vide] = res
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    ### VISUALISATION ######################################################
    
    elif choix == "18":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            automaton.edit_csv("buffer", automaton.matrix,automaton.final_states)
            # Ensure the output directory exists
            os.makedirs('output-png', exist_ok=True)

            # Paths for the CSV and the image file
            csv_path = 'Sample/buffer.csv'  # Replace with your actual CSV file path

            # Loop to find the next available file name
            counter = 1
            while os.path.exists(os.path.join('output-png', f'otomate{counter}')):
                counter += 1
            image_path = os.path.join('output-png', f'otomate{counter}')


            # Process the CSV file and save the automaton image
            draw_and_save_automaton(csv_path, image_path)
            image_path_with_extension = image_path + '.png'
            os.remove(image_path)
            webbrowser.open('file://' + os.path.realpath(image_path_with_extension))


            pass
            print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")
        
    #### JFF to CSV ###########################################################

    elif choix == "19":
        print("Vous voulez convertir un fichier .jff en .csv \n")
        jff_filename = input("Entrez le nom du fichier .jff  : ")
        csv_filename = input("Entrez le nom du fichier .csv  : ")
        jff_to_csv(jff_filename, csv_filename)

    #### MANUEL ###########################################################

    elif choix == "20":
        display_manual()

    # ### EXIT #############################################################
        
    elif choix == "21":
        qu = input("Après avoir quitté, vos automates seront supprimés des slots.\nAvez-vous bien exporté tous les automates que vous vouliez ? (0/N) \n")
        if qu in ["O","OUI","Oui","o","oui","Yes","Y","y","yes","YES"]:
            print("Merci et à bientôt !")
            break
        else:
            print("\nRetour au menu principal.\n")
    else:
        print("\nChoix invalide. Veuillez réessayer.\n")
