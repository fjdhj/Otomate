from automate import automate


#class Automate:
#    def __init__(self, nom, etats, transitions, liaisons):
#        self.nom = nom
#        self.etats = etats
#        self.transitions = transitions
#        self.liaisons = liaisons


def modifier_automate(automate):
    # Menu de modification d'automate
    while True:
        print("\nMenu de modification d'automate :")
        print("1. Changement de nom")
        print("2. Rajouter un état")
        print("3. Supprimer un état")
        print("4. Ajouter une transition")
        print("5. Supprimer une transition")
        print("6. Ajouter une liaison")
        print("7. Supprimer une liaison")
        print("8. Revenir au menu principal")

        choix_modification = input("Choisissez une action : ")

        if choix_modification == "1":
            nouveau_nom = input("Entrez le nouveau nom de l'automate : ")
            automate.nom = nouveau_nom
        elif choix_modification == "2":
            # Logique pour rajouter un état
            pass
        elif choix_modification == "3":
            # Logique pour supprimer un état
            pass
        elif choix_modification == "4":
            # Logique pour ajouter une transition
            pass
        elif choix_modification == "5":
            # Logique pour supprimer une transition
            pass
        elif choix_modification == "6":
            # Logique pour ajouter une liaison
            pass
        elif choix_modification == "7":
            # Logique pour supprimer une liaison
            pass
        elif choix_modification == "8":
            break
        else:
            print("Choix invalide. Veuillez réessayer.")



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
    
    if choix == "1":
        file_name=str(input("Type the file name to import automaton:\n"))
        new_automaton=automate(file_name)
        slots[slot_vide] = new_automaton 
        print(slots)
    
    ### EXPORTATION ##############################################################
        
    elif choix == "2":
        slot = int(input("Entrez le numéro du slot (1-10) : "))
        
        automaton = slots[slot - 1]
        if automaton:
            file_name=str(input("Type the file name to export automaton:\n"))
            automaton.edit_csv(file_name)
        else:
            print("No automaton in the slot.")
            
            
    # ### CREATION #################################################################
            
    # elif choix == "3":
    #     if slot_vide is not None:
    #         slots[slot_vide] = creer_automate()
    # else:
    #     print("Aucun slot disponible pour créer un nouvel automate.")
    
    # ### MODIFICATION ############################################################
            
    # elif choix == "4":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         modifier_automate(automate)
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### SUPPRESSION #############################################################
            
    # elif choix == "5":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     #supprimer_aef(slot)
        
        
    # ### PASSER UN MOT ###########################################################
        
    # elif choix == "6":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         mot = input("Entrez le mot à vérifier : ")
    #         #passer_mot(automate, mot)
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### AUTOMATE COMPLET #######################################################
            
    # elif choix == "7":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #res = automate_complet(automate)
    #         #if res != None:
    #             #slot[slot_vide] = res
    #     else:
    #         print("Aucun automate dans ce slot.")
            
    
    # ### AUTOMATE DETERMINISTE #################################################
            
    # elif choix == "8":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #res = automate_deterministe(automate)
    #         #if res != None:
    #             #slot[slot_vide] = res
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
    # ### AUTOMATE MIROIR ######################################################
            
    # elif choix == "9":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #slot[slot_vide] = miroir(automate)
    #     else:
    #         print("Aucun automate dans ce slot.")
            
        
    # ### AUTOMATE COMPLEMENTAIRE #############################################
            
    # elif choix == "10":
    #     slot = int(input("Entrez le numéro du slot (1-10) : "))
    #     automate = slots_automates[slot - 1]
    #     if automate:
    #         #slot[slot_vide] = complément(automate)
    #     else:
    #         print("Aucun automate dans un des slots sélectionnés.")
    
    
    # ### PRODUIT D'AUTOMATES #################################################
            
    # elif choix == "11":
    #     slot = int(input("Entrez le numéro du slot (1-10) du premier automate : "))
    #     automate1 = slots_automates[slot - 1]
    #     slot = int(input("Entrez le numéro du slot (1-10) du second automate : "))
    #     automate2 = slots_automates[slot - 1]
    #     if automate1 & automate2:
    #         #res = produit(automate1,automate2)
    #         #if res != None:
    #             #slot[slot_vide] = res
    #     else:
    #         print("Aucun automate dans ce slot.")
            
            
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
