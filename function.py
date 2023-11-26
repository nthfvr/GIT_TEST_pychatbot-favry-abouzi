import os
import math
def list_of_files(directory, extension):

    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

directory = "./speeches"
files_names = list_of_files(directory, "txt")
print(files_names)



# Fonction pour convertir le texte en minuscules
def minuscule():
    # on recupere les noms des fichier dans "speeches"
    files_names = list_of_files("speeches", "txt")

    # Parcours de chaque fichier
    for names in files_names:
        # Ouverture du fichier d'origine en mode lecture et du fichier résultant en mode écriture
        with open("speeches\\" + names, "r", encoding="utf-8") as fichier_president, open(
                "cleaned\\" + names + "cleaned.txt", "w", encoding="utf-8") as fichier_minuscule:
            # Lecture du contenu du fichier d'origine
            contenu = fichier_president.readlines()
            resultat = []

            # Parcours de chaque ligne dans le fichier d'origine
            for chaine in contenu:
                chaine_convertie = ""

                # Parcours de chaque caractère dans la ligne
                for caractere in chaine:
                    # Vérification si le caractère est une lettre majuscule
                    if 'A' <= caractere <= 'Z':
                        # Conversion en minuscule en ajustant le code ASCII
                        chaine_convertie += chr(ord(caractere) + (ord('a') - ord('A')))
                    else:
                        chaine_convertie += caractere

                # Ajout de la ligne convertie dans la liste des résultats
                resultat.append(chaine_convertie)

            # Écriture du contenu converti dans le fichier résultant
            for ligne in resultat:
                fichier_minuscule.write(ligne)


# Fonction pour supprimer la ponctuation
def ponctuation():
    texte_nettoye = ""
    list_ponctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                        '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

    # Liste des noms de fichiers dans le répertoire "cleaned"
    files_names = list_of_files("cleaned", "txt")

    # Parcours de chaque fichier
    for names in files_names:
        # Ouverture du fichier à nettoyer en mode lecture
        with open("cleaned\\" + names, "r", encoding="utf-8") as fichier_cleaned:
            contenu = fichier_cleaned.readlines()

            # Parcours de chaque ligne dans le fichier à nettoyer
            for chaine in contenu:
                # Parcours de chaque caractère dans la ligne
                for caractere in chaine:
                    # Remplacement des tirets et apostrophes par des espaces
                    if caractere == '-' or caractere == "'":
                        texte_nettoye += " "
                    # Ajout du caractère dans le résultat s'il n'est pas dans la liste de ponctuation
                    elif caractere not in list_ponctuation:
                        texte_nettoye += caractere

            # Écriture du texte nettoyé dans le même fichier
            with open("cleaned\\" + names, "w", encoding="utf-8") as fichier_cleaned:
                fichier_cleaned.write(texte_nettoye)
                texte_nettoye = ""


def noms_presidents(noms_fichiers):
    # Renvoie une liste des noms des présidents à partir des noms des fichiers.
    liste_presidents = []

    # Supprime les prefixes "Nomination_" et suffixes ".txt"  des noms des fichiers.
    for i in range(len(noms_fichiers)):
        noms_fichiers[i] = noms_fichiers[i].strip("Nomination_")
        noms_fichiers[i] = noms_fichiers[i].strip(".txt")
        noms_fichiers[i] = noms_fichiers[i].strip("cleanedtxt")

    # Supprime tous les caractères qui ne font pas partie de l'alphabet dans les noms des présidents.
    for nom in noms_fichiers:
        nouveau_nom = ""
        for letter in nom:
            if letter.isalpha():
                nouveau_nom += letter
        liste_presidents.append(nouveau_nom)

    dictionnaire_presidents = dict.fromkeys(set(liste_presidents))
    return liste_presidents,dictionnaire_presidents

def tf(chaine):
#Renvoie le nombre d'occurences de chaque mot dans un fichier

    dictionnaire_mot = {}
    liste_mots = chaine.split()
    liste_mots_sans_doublon = set(liste_mots)

    for word in liste_mots_sans_doublon:
        valeur = 0
        for mot_correspondant in liste_mots:
            if word == mot_correspondant:
                valeur += 1
        dictionnaire_mot[word] = valeur


    return dictionnaire_mot


noms_fichiers = list_of_files("speeches", "txt")
noms_presidentss, dictionnaire_president = noms_presidents(noms_fichiers)

# Appel des fonctions
minuscule()
ponctuation()




# Fonction qui calcule le score IDF pour chaque mot dans un répertoire de fichiers texte
def IDF(repertoire):
    # Récupération de la liste des noms de fichiers texte dans le répertoire
    files_names = list_of_files(repertoire, "txt")
    # Initialisation d'un ensemble pour stocker tous les mots uniques dans les documents
    set_mots = set([])
    # Initialisation du nombre total de documents
    nb_doc = 0
    # Boucle pour parcourir chaque fichier dans le répertoire
    for names in files_names:
        # Lecture du contenu du fichier
        with open(repertoire + names, "r", encoding="utf-8") as fichier_cleaned:
            contenu = fichier_cleaned.read()
            # Division du contenu en une liste de mots
            liste_de_mots = contenu.split()
            # Ajout de chaque mot à l'ensemble des mots uniques
            for mots in liste_de_mots:
                set_mots.add(mots)
            # Incrémentation du nombre de documents
            nb_doc += 1
    # Initialisation d'un dictionnaire pour stocker le nombre d'occurrences de chaque mot dans les documents
    dico_occurence_mot = {}
    # Boucle pour chaque mot unique dans l'ensemble de mots
    for mots in set_mots:
        # Initialisation du compteur d'occurrences pour le mot en cours
        cpt_occu_doc = 0
        # Boucle pour chaque fichier dans le répertoire
        for names in files_names:
            # Lecture du contenu du fichier
            with open(repertoire + names, "r", encoding="utf-8") as fichier_cleaned:
                contenu = fichier_cleaned.read()
                # Division du contenu en une liste de mots
                liste_de_mots = contenu.split()
                # Vérification de l'occurrence du mot dans le fichier
                if mots in liste_de_mots:
                    cpt_occu_doc += 1
        # Stockage du nombre d'occurrences du mot dans le dictionnaire
        dico_occurence_mot[mots] = cpt_occu_doc
    # Initialisation d'un dictionnaire pour stocker le score IDF de chaque mot
    score_idf = {}
    # Boucle pour chaque mot dans le dictionnaire d'occurrences
    for cle in dico_occurence_mot.keys():
        # Calcul du score IDF et stockage dans le dictionnaire
        score_idf[cle] = math.log((nb_doc / dico_occurence_mot[cle])+1, 10)
    # Retourne le dictionnaire final des scores IDF pour chaque mot
    return score_idf
IDF("cleaned\\")






def calculer_tfidf(repertoire):
    files_names = list_of_files(repertoire, "txt")
    set_mots = []
    for names in files_names:
        with open(repertoire + names, "r", encoding="utf-8") as fichier_cleaned:
            contenu = fichier_cleaned.read()
            liste_de_mots = contenu.split()
            for mots in liste_de_mots:
                set_mots.append(mots)
    set_mots=list(set(set_mots))


    idf=IDF("cleaned\\")

    matrice_tfidf = [[] for i in range(len(set_mots))]
    i=0
    for names in files_names:
        i=0
        mot_du_fichier = set([])
        with open("cleaned\\" + names, "r", encoding="utf-8") as fichier_cleaned:
            contenu = fichier_cleaned.read()
            tf_fichier = tf(contenu)
            liste_de_mots = contenu.split()
            for mots in liste_de_mots:
                mot_du_fichier.add(mots)
            for mot in set_mots:
                if mot in mot_du_fichier:
                    tf_mot=tf_fichier[mot]
                    idf_mot=idf[mot]
                    matrice_tfidf[i].append(tf_mot*idf_mot)
                else :
                    matrice_tfidf[i].append(0)
                i+=1
    #creation dictionaire pour associer le mot a ses scores tf-idf
    dico_matrice={}
    for i in range(len(set_mots)):
        dico_matrice[set_mots[i]]=matrice_tfidf[i]





    return [(matrice_tfidf), dico_matrice]







## Fonctionalité à developper
tfidf=(calculer_tfidf("cleaned\\"))

def mot_non_important(repertoire):
    files_names=list_of_files(repertoire, "txt")
    list_mot_0 = [k for (k, val) in tfidf[1].items() if val==[0 for i in range(len(files_names))]]
    return (list_mot_0)

def mot_max_occurrences(mot):
    # Liste des fichiers dans le répertoire cleaned
    files_names = list_of_files("./speeches", ".txt")

    # Initialisation des variables pour le fichier avec le plus grand nombre d'occurrences
    fichier_max_occurrences = ""
    max_occurrences = 0

    # Liste pour stocker les fichiers contenants le mot de recherche
    fichiers_avec_mot = []

    for filename in files_names:
        # Construire le chemin complet du fichier
        chemin_fichier = os.path.join("./speeches", filename)

        # Lire le contenu du fichier
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()

            # Utiliser la fonction tf() pour obtenir le nombre d'occurrences du mot de recherche
            occurrences_mot = tf(contenu).get(mot,0)


            # Vérifier si le mot de recherche est présent dans le fichier
            if occurrences_mot > 0:
                fichiers_avec_mot.append(filename)

            # Mettre à jour le fichier avec le plus grand nombre d'occurrences si nécessaire
            if occurrences_mot > max_occurrences:
                max_occurrences = occurrences_mot
                fichier_max_occurrences = filename

    return fichiers_avec_mot, fichier_max_occurrences




def premier_president_ecologie_climat(directory, extension):
    # Liste des fichiers dans le répertoire avec l'extension spécifiée
    noms_fichier_local = list_of_files(directory, extension)

    # Initialiser le nom du premier président à parler d'écologie ou de climat
    premier_president_ecologie_climat = ""

    for filename in noms_fichier_local:
        liste_temp = []
        # Construire le chemin complet du fichier
        chemin_fichier = os.path.join(directory, filename)

        # Lire le contenu du fichier
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            contenu_president = fichier.read()
            #ajoute le nom du fichier à une liste pour pouvoir utiliser la fonction nom président dessus
            liste_temp.append(filename)
            # Vérifier si le fichier mentionne l'écologie ou le climat
            if 'écologie' in contenu_president or 'climat' in contenu_president:
                premier_president_ecologie_climat = noms_presidents(liste_temp)[0][0]
                break  # Sortir de la boucle dès qu'un président est trouvé

    return premier_president_ecologie_climat

directory = "cleaned"
extension = "txt"
resultat = premier_president_ecologie_climat(directory, extension)

if resultat:
    print(f"Le premier président à parler d'écologie ou de climat est : {resultat}")
else:
    print("Aucun président ne mentionne l'écologie ou le climat.")





def choix():
    print("---------------------------------------------------------------------------------------------------------------------------")
    print("Sélectionner une option :")
    print("1 :Afficher la liste des mots les moins importants dans le corpus de documents")
    print("2 :Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé")
    print("3 :Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac")
    print("4 :Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois")
    print("5 :Indiquer le premier président à parler du climat et/ou de l’écologie")
    print("6 :Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués.")
    print("---------------------------------------------------------------------------------------------------------------------------")
    liste_choix = [str(i) for i in range(1,7)]
    choix = None
    while not choix in liste_choix:
        choix = input("Quel est votre choix: ")
    return choix

def menu():
    running = True
    while running:
        choix_utilisateur = choix()
        match choix_utilisateur:
            case "1":
                print(mot_non_important("cleaned"))
            case "1" :
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                resultat = premier_president_ecologie_climat("cleaned",".txt")
                if resultat:
                    print(f"Le premier président à parler d'écologie ou de climat est : {resultat}")
                else:
                    print("Aucun président ne mentionne l'écologie ou le climat.")

            case other:
                choix_utilisateur = choix()

menu()