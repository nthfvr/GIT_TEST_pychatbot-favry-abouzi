import os
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

    # Supprime tous les caractères qui ne font pas partie de l'alphabet dans les noms des présidents.
    for nom in noms_fichiers:
        nouveau_nom = ""
        for letter in nom:
            if letter.isalpha():
                nouveau_nom += letter
        liste_presidents.append(nouveau_nom)

    dictionnaire_presidents = dict.fromkeys(set(liste_presidents))
    return liste_presidents,dictionnaire_presidents

def tf(fichier):
#Renvoie le nombre d'occurences de chaque mot dans un fichier
    with open(fichier, 'r', encoding='utf-8') as file:
        chaine = file.read()
    liste_occurences = []
    dictionnaire_mot = {}
    dictionnaire_tf = {}
    liste_mots = chaine.split()
    liste_mots_sans_doublon = list(set(liste_mots))



    for word in liste_mots_sans_doublon:
        liste_occurences.append(liste_mots.count((word)))

    for i in range(len(liste_mots_sans_doublon)):
        cle = liste_mots[i]
        valeur = liste_occurences[i]
        dictionnaire_mot[cle] = valeur


    return dictionnaire_mot


noms_fichiers = list_of_files("speeches", "txt")
noms_presidents, dictionnaire_president = noms_presidents(noms_fichiers)

# Appel des fonctions
minuscule()
ponctuation()

import math


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
        score_idf[cle] = math.log(nb_doc / dico_occurence_mot[cle], 10)
    # Retourne le dictionnaire final des scores IDF pour chaque mot
    return score_idf




def TF_IDF():
    matrice_tfidf=[]
    # Récupération de la liste des noms de fichiers texte dans le répertoire
    files_names = list_of_files("cleaned\\", "txt")
    # Initialisation d'un ensemble pour stocker tous les mots uniques dans les documents
    set_mots = set([])
    # Initialisation du nombre total de documents
    nb_doc = 0
    # Boucle pour parcourir chaque fichier dans le répertoire
    for names in files_names:
        # Lecture du contenu du fichier
        with open("cleaned\\" + names, "r", encoding="utf-8") as fichier_cleaned:
            contenu = fichier_cleaned.read()
            # Division du contenu en une liste de mots
            liste_de_mots = contenu.split()
            # Ajout de chaque mot à l'ensemble des mots uniques
            for mots in liste_de_mots:
                set_mots.add(mots)
            # Incrémentation du nombre de documents
            nb_doc += 1
    set_IDF=IDF("cleaned\\")
    for mot in set_mots :
        liste_inter=[]
        for names in files_names:
            with open("cleaned\\" + names, "r", encoding="utf-8") as fichier_cleaned:
                contenu = fichier_cleaned.read()
                liste_de_mots = contenu.split()
                set_mots_fichier=set(liste_de_mots)
                set_tf = tf("cleaned\\" + names)

                if mot in set_tf:
                    tf_mot=set_tf[mot]
                else :
                    tf_mot=0

                idf_mot=set_IDF[mot]
                tf_idf_mot=tf_mot*idf_mot
                liste_inter.append(tf_idf_mot)


        matrice_tfidf.append(liste_inter)
    print(matrice_tfidf)






TF_IDF()