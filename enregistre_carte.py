#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
enregistre_carte.py
"""

import sqlite3 
import lire_carte

def enregistre():
    """
    Enregistrement d'une carte nfc dans la BDD
    """
    carte_etu = lire_carte.lecture_carte()

    uid = carte_etu['uid']
    jour = carte_etu['jour']
    heure = carte_etu['heure']
    nom = carte_etu['nom']
    prenom = carte_etu['prenom']
    groupe = carte_etu['groupe']

    cursor.execute('SELECT uid FROM Etudiants')
    liste_uid = cursor.fetchall()

    #Test si les valeurs sont connues
    ajout = 0
    for uid in liste_uid:

        if uid != uid[0]:    
            ajout = 1        #Valeurs a ajoutées        
        else:
            ajout = 0
            print "UID déjà existant"    
            cursor.execute("""UPDATE Etudiants SET groupe = ? WHERE uid = ?""", (groupe, uid, ))
            break

    if ajout != 0:     
        cursor.execute('''INSERT INTO Etudiants(uid, jour, heure, nom, prenom, groupe)
        VALUES(?, ?, ?, ?, ?, ?)''', (uid, jour, heure, nom, prenom, groupe))    
        print "Les valeurs ont été ajoutées"

#Connexion a la bdd
connection = sqlite3.connect('carte.db')
print "\nOuverture de la base de données"

cursor = connection.cursor()

#Creation de la table
cursor.execute("CREATE TABLE IF NOT EXISTS Etudiants(id INTEGER PRIMARY KEY, uid VARCHAR, jour DATE, heure TIME, nom VARCHAR, prenom VARCHAR, groupe VARCHAR)")
print "Table créée"

#Boucle pour lire ou non carte
rep = raw_input("Enregistrer une carte ?(O:oui/N:non)")
liste = ['o', 'O', '0']
while rep in liste:
    enregistre()
    rep = raw_input("\nEnregistrer une carte ? (O:oui/N:non)")

connection.commit()

#Ecriture des données
cursor.execute('SELECT * FROM Etudiants')

for i in cursor:
    print "*****\n"
    print "ID: ", i[0]
    print "UID: ", i[1]
    print "Jour: ", i[2]
    print "Heure: ", i[3]
    print "Nom: ", i[4]
    print "Prenom: ", i[5]
    print "Groupe: ", i[6]

cursor.close()