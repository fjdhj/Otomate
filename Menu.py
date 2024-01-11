#Importations
from automate import automate
from convertCsvPng import draw_and_save_automaton
from convertJffCsv import jff_to_csv
import datetime
import os
import webbrowser


def saisir_numero_slot():
    """
    Fonction qui demande un numéro de slot valide à l'utilisateur.
    Vérifie la validité des arguments.
    
    Args: None

    Returns:
        slot : int (error = -1) 
    """
    while True:
        try:
            #Vérifie que le slot choisi est bien entre 1 et 10 compris
            slot = int(input("Entrez le numéro du slot (1-10) : "))
            if 1 <= slot <= 10:
                return slot  # Renvoyer le slot valide
            else:
                print("Veuillez entrer un nombre entre 1 et 10.\n")
        except ValueError:
            #Si une ValueError est détectée, c'est que l'utilisateur a rempli autre chose qu'un entier
            #Alors on renvoie une valeur d'erreur
            print("Veuillez entrer un nombre entier valide.\n")
            return -1


def modifier_automate(actual_auto:automate):
    """
    Procédure de modification d'un automate.
    Demande à l'utilisateur ce qu'il veut modifier, puis applique la modification.
    Sous-menu du menu principal, qu'on peut rejoindre avec la dernière option.
    
    Args:
        actual_auto : automate
    
    Returns: None
    """
    
    while True:
        #On affiche le menu de modification
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
            #On applique la méthode de création d'état de Automate
            state_name = str(input("Entrez le nom du nouvel état : "))
            actual_auto.create_state(state_name)
            
        elif choix_modification == "2":
            #On applique la méthode de suppression d'état de Automate
            state_name = str(input("Entrez le nom de l'état à supprimer : "))
            actual_auto.delete_state(state_name)
            
        elif choix_modification == "3":
            #On applique la méthode de création de transition de Automate
            transition_name = str(input("Entrez le nom de la nouvelle transition : "))
            actual_auto.create_transition(transition_name)
            
        elif choix_modification == "4":
            #On applique la méthode de suppression de transition de Automate
            transition_name = str(input("Entrez le nom de la transition à supprimer : "))
            actual_auto.delete_transition(transition_name)
            
        elif choix_modification == "5":
            #On demande l'état de départ et on le crée si besoin
            initial_state_name = str(input("Entrez le nom de l'état de départ : "))
            if not (initial_state_name in actual_auto.all_states):
                actual_auto.create_state(initial_state_name)
            
            #On demande l'état d'arrivée et on le crée si besoin    
            final_state_name = str(input("Entrez le nom de l'état d'arrivée : "))
            if not (initial_state_name in actual_auto.all_states):
                actual_auto.create_state(final_state_name)
            
            #On demande la transition utilisée et on la crée si besoin    
            transition_name = str(input("Entrez le nom de la transition : "))
            if not (transition_name in actual_auto.transitions):
                actual_auto.create_transition(transition_name)
            
            #On ajoute la liaison en fonction des entrées précédentes    
            actual_auto.add_transition(initial_state_name, transition_name, final_state_name)
            
        elif choix_modification == "6":
            #On demande l'état de départ et on vérifie qu'il existe
            initial_state_name = str(input("Entrez le nom de l'état de départ : "))
            if not (initial_state_name in actual_auto.all_states):
                while(not (initial_state_name in actual_auto.all_states)):
                    print("Cet état n'existe pas")
                    initial_state_name = str(input("Entrez le nom de l'état de départ : "))
                
            #On demande l'état d'arrivée et on vérifie qu'il existe
            final_state_name = str(input("Entrez le nom de l'état d'arrivée : "))
            if not (initial_state_name in actual_auto.all_states):
                while(not (initial_state_name in actual_auto.all_states)):
                    print("Cet état n'existe pas")
                    final_state_name = str(input("Entrez le nom de l'état d'arrivée : "))

            #On demande la transition et on vérifie qu'elle existe
            transition_name = str(input("Entrez le nom de la transition : "))
            if not (transition_name in actual_auto.transitions):
                while(not (transition_name in actual_auto.transitions)):
                    print("Cette transition n'existe pas")
                    transition_name = str(input("Entrez le nom de la transition : "))
            
            #On supprime la liaison
            actual_auto.remove_transition(initial_state_name, transition_name, final_state_name)

        elif choix_modification == "7":
            # Display initial states and allow modification
            print("Ci-dessous la liste des états initiaux\n")
            # Iterating through all states to find and display initial states
            for i in range(len(actual_auto.initial_states)):
                if(actual_auto.initial_states[i] == 1):
                    print(actual_auto.all_states[i])
            # User chooses a state to modify its initial status
            state = input("Choisissez un état\n")
            index_state = actual_auto.all_states.index(state)
            # Check if the chosen state is currently an initial state
            if(actual_auto.initial_states[index_state] == 1):
                # Ask user if they want to change the state from initial to non-initial
                if(input("Cet état est actuellement initial, le rendre non-initial ? y/n\n") == "y"):
                   actual_auto.demake_initial(state)
            else:
                # Ask user if they want to change the state from non-initial to initial
                if(input("Cet état est actuellement non-initial, le rendre initial ? y/n\n") == "y"):
                    actual_auto.make_initial(state) # Make the state initial
        elif choix_modification == "8":
            # Display final states and allow the user to modify them
            print("Ci-dessous la liste des états finaux\n")
            # Iterating through all states to find and display final states
            for i in range(len(actual_auto.final_states)):
                if(actual_auto.final_states[i] == 1):
                    print(actual_auto.all_states[i])
            # User chooses a state to modify its final status
            state = input("Choisissez un état\n")
            index_state = actual_auto.all_states.index(state)
            # Check if the chosen state is currently a final state
            if(actual_auto.final_states[index_state] == 1):
                # Ask user if they want to change the state from final to non-final
                if(input("Cet état est actuellement final, le rendre non-final ? y/n\n") == "y"):
                   actual_auto.demake_final(state)  # Make the state non-final
            else:
                # Ask user if they want to change the state from non-final to final
                if(input("Cet état est actuellement non-final, le rendre final ? y/n\n") == "y"):
                    actual_auto.make_final(state) # Make the state final
        elif choix_modification == "9":
            break
        else:
            print("Choix invalide. Veuillez réessayer.\n")

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
    

def print_timestamp():
    """
    Formate l'heure actuelle.
    
    Args: None

    Returns:
        formatted_time : string
    """
    
    #Récupère l'heure actuelle
    current_time = datetime.datetime.now()
    #Formate la datge
    formatted_time = current_time.strftime("%Y-%m-%d %H_%M_%S")
    #Renvoie le formatage
    return formatted_time

##########################################################################################
################################## Menu principal ########################################
##########################################################################################


# Instancie la liste des automates en traitement
slots:list = [None] * 10

while True:
    
    #Instancie les variables temporaires d'automate à None
    automaton=None
    automaton1=None
    automaton2=None
    bouclesuivante=0
    
    #Affiche le contenu des slots
    i=0
    for auto in slots:
        #On vérifie si l'automate est instancié ou pas dans le slot
        if auto is not None:
            print("Slot ",i+1," : ", auto.name)
        else :
            print("Slot ",i+1," : None")
        i+=1
    print ("\n")
    
    # Trouve le prochain slot vide (NONE si complet)
    slot_vide = next((i for i, automate in enumerate(slots) if automate is None), None)
    
    
    ### GESTION DES SLOTS ################################################################
    

    while slot_vide == None:
        #Si aucun slot n'est disponible, on demande à l'utilisateur d'exporter ou de supprimer un automate d'un slot
        print ("Aucun slot de disponible. Veuillez en supprimer un ou l'exporter.")
        print("1. Supprimer un automate\n2. Exporter un automate\n")
        
        choix = input("Choisissez une action : ")
        print("\n")
        
        if choix == "1":
            slot = saisir_numero_slot()
            #S'il n'y a pas d'erreur...
            if slot != -1 : 
                #... On supprime l'automate correspondant au slot
                slots[slot - 1] = None
                print("Suppression effectuée.\n\n")
                #bouclesuivante permet plus tard de retourner au début du menu
                bouclesuivante=1
                
        elif choix == "2":
            slot = saisir_numero_slot()
            #On applique la même méthode que dans le menu principal
            if slot != -1 and slots[slot-1] != None:
                automaton :automate= slots[slot - 1]
                file_name=str(input("Type the file name to export automaton: "))
                if file_name.endswith(".csv"):
                    file_name=file_name.rstrip(".csv")
                path = os.path.dirname(file_name) + "/"
                basename = os.path.basename(file_name)
                if not os.path.exists(path):
                    print(f"Le chemin '{file_name}' n'existe pas.\n")
                else:
                    automaton.edit_csv(basename, automaton.matrix,automaton.final_states)
                    print("Traitement effectué.\n\n")      
            else:
                print("Slot invalide. Veuillez réessayer.\n")
            
        #On recalculte si on slot a bien été libéré
        slot_vide = next((i for i, automate in enumerate(slots) if automate is None), None)
    
    #On sort de l'occurence actuelle si un slot a bien été libéré
    if bouclesuivante==1:
        continue
            
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
    
    if choix == "1":
        if slot_vide is not None:
            #On demande la chemin du fichier où enregistrer l'automate
            file_name=str(input("Type the file name to import automaton: "))
            
            #S'il manque l'extension .csv on la rajoute
            if not file_name.endswith(".csv"):
                file_name += ".csv"
            
            #Si le chemin n'existe pas, on met un message d'erreur
            if not os.path.exists(file_name):
                print(f"Le fichier '{file_name}' n'existe pas.\n")
            
            #Sinon on crée l'automate dans le prochain slot vide
            else:
                slots[slot_vide] = automate(file_name) 
                print(slots)
                print("Automate enregistré dans le slot : ",slot_vide+1,"\n\n")
                
        else:
            print("Aucun slot disponible pour créer un nouvel automate.\n")  
    
    ### EXPORTATION ##############################################################
        
    elif choix == "2":
        
        slot = saisir_numero_slot()
        
        #On vérifie que le slot est bien valide, et qu'il n'est pas vide
        if slot != -1 and slots[slot-1] != None:
            automaton :automate= slots[slot - 1]
            
            #On demande où est l'automate à importer
            file_name=str(input("Type the file name to export automaton: "))
            
            #On rajoute l'extension .csv si besoin
            if file_name.endswith(".csv"):
                file_name=file_name.rstrip(".csv")
            
            #On vérifie l'existence du chemin et on affiche un message d'erreur si besoin
            path = os.path.dirname(file_name) + "/"
            basename = os.path.basename(file_name)
            if not os.path.exists(path):
                print(f"Le chemin '{file_name}' n'existe pas.\n")
            #Si tout est bon on édite le fichier
            else:
                automaton.edit_csv(basename, automaton.matrix,automaton.final_states)
                print("Traitement effectué.\n\n")
                
        else:
            print("Slot invalide. Veuillez réessayer.\n")
            
    # ### CREATION #################################################################
     
    elif choix == "3":
        
        if slot_vide is not None:
            
            #On demande le chemin du fichier où créer l'automate
            file_name=str(input("Type the file name to create automaton: "))
            
            #On rajoute l'extension si besoin
            if not file_name.endswith(".csv"):
                file_name+=".csv"
                
            #On vérifie l'existence du chemin
            dir = os.path.dirname(file_name)
            if not os.path.exists(dir) and dir!="":
                print(f"Le chemin '{file_name}' n'existe pas.\n")
            #Si tout est bon on crée le fichier et l'automate qu'on met dans le prochain slot vide
            else:
                slots[slot_vide] = automate(file_name)
                print(slots)
                print("Traitement effectué.\n\n")
                
        else:
            print("Aucun slot disponible pour créer un nouvel automate.\n")   
    
    # ### MODIFICATION ############################################################
            
    elif choix == "4":
        
        slot = saisir_numero_slot()
        if slot != -1 :
            
            #On récupère l'automate correspondant
            automaton = slots[slot - 1]
            
            #Si l'automate existe bien, on ouvre le menu de modification
            if automaton:
                modifier_automate(automaton)
                print("Traitement effectué.\n\n")
            
            else:
                print("Aucun automate dans ce slot.\n")
            
            
    # ### SUPPRESSION #############################################################
            
    elif choix == "5":
        
        slot = saisir_numero_slot()
        if slot != -1 :
            
            #On écrase l'automate correspondant au slot fourni
            slots[slot - 1] = None
            print("Suppression effectuée.\n\n")
        
        
    # ### PASSER UN MOT ###########################################################
        
    elif choix == "6":
        
        #On récupère le slot et l'automate correspondant
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton: automate = slots[slot - 1]
        
            #Si l'automate existe... et est déterministe
            if automaton and automaton.is_deterministic():
                #...On récupère le mot à vérifier
                print(automaton.is_deterministic())
                qu = input("Ecrivez un mot à reconnaitre pour l'automate: \n")
                
                #On vérifie si le mot est reconnu, et on affiche le résultat
                recognize=automaton.recognize_wordAFD(qu)
                if recognize:
                    print("Le mot est reconnu.\n")
                else:
                    print("Le mot n'est pas reconnu.\n")
            elif automaton and not automaton.is_deterministic():  
                # On le déterminise et on reconnait le mot    
                if(input("L'automate n'est pas déterministe, voulez-vous le rendre déterministe ? [Y/N]\n") == "Y"):
                   
                    
                    auto=automaton.AND_to_AFD()
                    print("Traitement effectué.\n\n")
                    qu = input("Ecrivez un mot à reconnaitre pour l'automate: \n")
        
                    #On vérifie si le mot est reconnu, et on affiche le résultat
                    recognize=automaton.recognize_wordAFD(qu)
                    if recognize:
                        print("Le mot est reconnu.\n")
                    else:
                        print("Le mot n'est pas reconnu.\n")
            else:
                print("Aucun automate dans le slot.\n")
            
            
    # ### AUTOMATE COMPLET #######################################################
            
    elif choix == "7":
        
        #On récupère le slot et l'automate correspondant
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton = slots[slot - 1]
            
            #Si l'automate existe...
            if automaton:
                #...on vérifie s'il est complet. Si oui, on affiche qu'il l'est et on sort.
                if(automaton.is_complete()):
                    print("L'automate est complet.")
                    
                else:
                    #Si l'automate n'est pas complet, on propose à l'utilisateur de le rendre complet.
                    if(input("L'automate n'est pas complet, voulez-vous le rendre complet ? [Y/N]\n") == "Y"):
                        automaton.make_complete()
                        print("Traitement effectué.\n\n")
                        
            else:
                print("Aucun automate dans ce slot.\n")
            
    
    # ### AUTOMATE DETERMINISTE #################################################
            
    elif choix == "8":
        
        #On récupère le slot et l'automate correspondant
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton = slots[slot - 1]
            
            #Si l'automate existe...
            if automaton:
                #... on vérifie s'il est déterministe. S'il l'est, on sort.
                if(automaton.is_deterministic()):
                    print("L'automate est déterministe.\n")
                    
                else:
                    #S'il ne l'est pas, on propose de le rendre déterministe.
                    if(input("L'automate n'est pas déterministe, voulez-vous le rendre déterministe ? [Y/N]\n") == "Y"):
                        auto=automaton.AND_to_AFD()
                        print("Traitement effectué.\n\n")
                        
            else:
                print("Aucun automate dans ce slot.\n")
            
            
    # ### AUTOMATE MIROIR ######################################################
            
    elif choix == "9":
        
        #On récupère l'automate correspondant au slot demandé
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton = slots[slot - 1]
            
            #Si l'automate existe, on enregistre son miroir
            if automaton:
                automaton.mirror()
                print("Traitement effectué.\n\n")
                
            else:
                print("Aucun automate dans ce slot.\n")
            
        
    # ### AUTOMATE COMPLEMENTAIRE #############################################
            
    elif choix == "10":
        
        #On récupère l'automate correspondant au slot demandé
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton = slots[slot - 1]
            
            #Si l'automate existe, on enregistre son complement
            if automaton:
                automaton.complement()
                print("Traitement effectué.\n\n")
                
            else:
                print("Aucun automate dans ce slot.\n")
    
    
    # ### PRODUIT D'AUTOMATES #################################################
            
    elif choix == "11":
        
        #On récupère le slot et l'automate correspondant
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton1 = slots[slot - 1]
            
            #On récupère le slot du deuxième automate
            slot = saisir_numero_slot()
            if slot != -1 :
                automaton2 = slots[slot - 1]
                
        #Si les deux automate existent, on enregistre leur produit dans le slot libre suivante
        if automaton1 and automaton2:
            slot_vide = next((i for i, automate in enumerate(slots) if automate is None), None)
            slots[slot_vide]=automaton1.product(automaton2)
            print("Automate enregistré dans le slot : ",slot_vide+1,"\n\n")
            print("Traitement effectué.\n\n")
            
        #Sinon, on affiche dans quel slot il y a une erreur
        else:
            if not (automaton1):
                print("Il n'y a aucun automate dans le premier slot.\n")
            elif not (automaton2):
                print("Il n'y a aucun automate dans le deuxième slot.\n")
            else:
                print("Il y a eu un problème.")
            
            
    # ### CONCATENATION ######################################################
            
    elif choix == "12":
        
        #On récupère le premier automate
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton1 = slots[slot - 1]
            
            #On récupère le deuxième automate
            slot = saisir_numero_slot()
            if slot != -1 :
                automaton2 = slots[slot - 1]
                
        #Si les deux automates existent, on les concatène dans le slot vide suivant
        if automaton1 and automaton2 :
            slot_vide = next((i for i, automate in enumerate(slots) if automate is None), None)
            automate_conca = automaton1.concatenate(automaton2)
            slots[slot_vide]=automate_conca
            print("Automate enregistré dans le slot : ",slot_vide,"\n\n")
            automate_conca.edit_csv("test", automate_conca.matrix, automate_conca.final_states)
            print("Traitement effectué.\n\n")
            
            
        else:
            print("Au moins l'un des automates n'existe pas dans les slots choisis.")
        
    ### EXTRAIRE EXPRESSION ################################################
            
    elif choix == "13":
        slot = saisir_numero_slot()
        if slot != -1:
            automate:automate = slots[slot - 1]
            if automate:
                print("L'expression régulière de cette automate est :", automate.get_regular_expression())
            else:
                print("Aucun automate dans ce slot.")
            
    # ### DETERMINER LANGAGE ################################################
            
    elif choix == "14":
        slot = saisir_numero_slot()
        if slot != -1 :
            automate = slots[slot - 1]
            if automate:
                print("Le langage de cette automate est : L = {%s}" % (automate.get_regular_expression()))
            else:
                print("Aucun automate dans ce slot.")
            
            
    # ### LANGAGES EQUIVALENTS ##############################################
            
    # elif choix == "15":
    #     slot = saisir_numero_slot()
    #     if slot != -1 :
    #         automate1 = slots_automates[slot - 1]
    #         slot = saisir_numero_slot()
    #         if slot != -1 :
    #             automate2 = slots_automates[slot - 1]
    #     if automate1 and automate2:
    #         #res = equivalence(automate1,automate2)
    #     else:
    #         print("Aucun automate dans un des slots.")
            
            
    # ### EMONDER AUTOMATE ##################################################
            
    elif choix == "16":
        slot = saisir_numero_slot()
        if slot != -1 :
            automate = slots[slot - 1]
            if automate:
                print("Vous avez choisi d'émonder l'automate\n")
                automate=automate.trim()
                print("Traitement effectué.\n\n")
            else:
                print("Aucun automate dans ce slot.")
            
            
    # ### RENDRE MINIMAL ###################################################
            
    # elif choix == "17":
    #     slot = saisir_numero_slot()
    #     if slot != -1 :
    #         automate = slots_automates[slot - 1]
    #         if automate:
    #             #res = minimal(automate)
    #             #if res != None:
    #                 #slot[slot_vide] = res
    #         else:
    #             print("Aucun automate dans ce slot.")
            
            
    ### VISUALISATION ######################################################
    
    elif choix == "18":
        slot = saisir_numero_slot()
        if slot != -1 :
            automaton = slots[slot - 1]
        else:
            automaton = None
        if automaton:
            automaton.edit_csv("buffer", automaton.matrix, automaton.final_states)
            # Ensure the output directory exists
            os.makedirs('output-png', exist_ok=True)

            # Define the CSV and image file paths
            csv_path = 'Sample/buffer.csv'  # Replace with your actual CSV file path
            timestamp = print_timestamp()
            image_filename = f'otomate_{timestamp}'

            # Set the image path with a timestamp
            image_path = os.path.join('output-png', image_filename)

            # Process the CSV file and save the automaton image
            draw_and_save_automaton(csv_path, image_path)
            image_path_with_extension = image_path + '.png'

            # Open the saved image in a web browser
            webbrowser.open('file://' + os.path.realpath(image_path_with_extension))

            #Erase .dot file
            os.remove('output-png/' + (image_filename))

            print("Traitement effectué.\n\n")
        else:
            print("Aucun automate dans ce slot.\n")

        
    #### JFF to CSV ########################################################

    elif choix == "19":
        
        #On demande les fichiers à convertir
        print("Vous voulez convertir un fichier .jff en .csv \n")
        jff_filename = input("Entrez le nom du fichier .jff  : ")
        csv_filename = input("Entrez le nom du fichier .csv  : ")
        
        #Si le chemin n'existe pas, on met un message d'erreur
        if not os.path.exists(jff_filename) and not os.path.exists(csv_filename):
            print(f"Un des fichiers n'existe pas.\n")
            
        #Sinon on applique la fonction
        else:
            jff_to_csv(jff_filename, csv_filename)

    #### MANUEL ############################################################

    elif choix == "20":
        
        #On affiche le manuel
        display_manual()

    # ### EXIT #############################################################
        
    elif choix == "21":
        
        #On demande si l'utisateur a bien effectué tout ce qu'il voulait faire avant de quitter
        qu = input("Après avoir quitté, vos automates seront supprimés des slots.\nAvez-vous bien exporté tous les automates que vous vouliez ? (O/N) \n")
        if qu in ["O","OUI","Oui","o","oui","Yes","Y","y","yes","YES"]:
            #Si oui, on quitte
            print("Merci et à bientôt !")
            break
        
        #Sinon on retourne au menu principal
        else:
            print("\nRetour au menu principal.\n")
            
            
    #Affiche de message d'erreur en cas de choix invalide
    else:
        print("\nChoix invalide. Veuillez réessayer.\n") 