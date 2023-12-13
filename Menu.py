from automate import automate


#class Automate:
#    def __init__(self, nom, etats, transitions, liaisons):
#        self.nom = nom
#        self.etats = etats
#        self.transitions = transitions
#        self.liaisons = liaisons


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
        print("7. Revenir au menu principal")

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
            break
        else:
            print("Choix invalide. Veuillez réessayer.\n")



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
    
    print("\nMenu principal :")
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
    print("18. Manuel")
    print("19. Quitter le programme")
    
    choix = input("Choisissez une action : ")


    ### IMPORTATION ##############################################################
    
    #FIXME NATHAN Si le paramètre entré ne correspond pas à un slot ça plante
    if choix == "1":
        if slot_vide is not None:
            file_name=str(input("Type the file name to import automaton:\n"))
            slots[slot_vide] = automate(file_name) 
            print(slots)
        else:
            print("Aucun slot disponible pour créer un nouvel automate.")  
    
    ### EXPORTATION ##############################################################
        
    elif choix == "2":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        is_deterministic:bool=str(input("Votre tableau est il un tableau que vous avez déterminiser [y/n]"))
        automaton :automate= slots[slot - 1]
        file_name=str(input("Type the file name to export automaton:\n"))
        automaton.edit_csv(file_name, automaton.matrix,automaton.final_states)
            
    # ### CREATION #################################################################
     
    elif choix == "3":
        if slot_vide is not None:
            file_name=str(input("Type the file name to import automaton:\n"))
            slots[slot_vide] = automate(file_name)
            print(slots)
        else:
            print("Aucun slot disponible pour créer un nouvel automate.")   
            
    # elif choix == "3":
    #     if slot_vide is not None:
    #         slots[slot_vide] = creer_automate()
    # else:
    #     print("Aucun slot disponible pour créer un nouvel automate.")
    
    # ### MODIFICATION ############################################################
            
    elif choix == "4":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            modifier_automate(automaton)
        else:
            print("Aucun automate dans ce slot.")
            
            
    # ### SUPPRESSION #############################################################
            
    elif choix == "5":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        slots[slot - 1] = None
        
        
    # ### PASSER UN MOT ###########################################################
        
    elif choix == "6":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton: automate = slots[slot - 1]
        if automaton:
            automaton.recognize_wordAFD(str(input("Entrez le mot à vérifier : \n")))
        else:
            print("Aucun automate dans ce slot.")
            
            
    # ### AUTOMATE COMPLET #######################################################
            
    elif choix == "7":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            if(automaton.is_complete()):
                print("L'automate est complet")
            else:
                if(input("L'automate n'est pas complet, voulez-vous le rendre complet ? [Y/N]\n") == "Y"):
                    automaton.make_complete()
        else:
            print("Aucun automate dans ce slot.")
            
    
    # ### AUTOMATE DETERMINISTE #################################################
            
    elif choix == "8":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            if(automaton.is_deterministic()):
                print("L'automate est déterministe")
            else:
                if(input("L'automate n'est pas déterministe, voulez-vous le rendre complet ? [Y/N]\n") == "Y"):
                    auto=automaton.AND_to_AFD()
        else:
            print("Aucun automate dans ce slot.")
            
            
    # ### AUTOMATE MIROIR ######################################################
            
    elif choix == "9":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            automaton.mirror()
        else:
            print("Aucun automate dans ce slot.")
            
        
    # ### AUTOMATE COMPLEMENTAIRE #############################################
            
    elif choix == "10":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        automaton = slots[slot - 1]
        if automaton:
            automaton.complement()
        else:
            print("Aucun automate dans ce slot.")
    
    
    # ### PRODUIT D'AUTOMATES #################################################
            
    elif choix == "11":
        slot = int(input("Entrez le numéro du slot (1-10) du premier automate : "))
        automaton1 = slots[slot - 1]
        slot = int(input("Entrez le numéro du slot (1-10) du second automate : "))
        automaton2 = slots[slot - 1]
        if automaton1 & automaton2:
            automaton1.product(automaton2)
        else:
            print("Aucun automate dans ce slot.")
            
            
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
            
            
    # ### MANUEL ###########################################################
            
    # elif choix == "18":
    #     #afficher_manuel()
        
        
    # ### EXIT #############################################################
        
    elif choix == "19":
        qu = input("Après avoir quitté, vos automates seront supprimés des slots.\nAvez-vous bien exporté tous les automates que vous vouliez ? (0/N) \n")
        if qu in ["O","OUI","Oui","o","oui","Yes","Y","y","yes","YES"]:
            print("Merci et à bientôt !")
            break
        else:
            print("Retour au menu principal.")
    else:
        print("Choix invalide. Veuillez réessayer.")
