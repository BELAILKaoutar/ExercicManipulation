import mysql.connector as mc

try:
    db = mc.connect(
        host="localhost",
        user="root",
        password="",  # Mettez votre mot de passe MySQL ici
        database="testmanip"
    )
    cursor = db.cursor()
except mc.Error as e:
    print("Erreur de connexion à la base de données:", e)
else:
    print("La connexion a été effectuée avec succès !")

def createTable():
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INT AUTO_INCREMENT PRIMARY KEY,
             nom TEXT,
             prenom TEXT,
             adresse TEXT,
             email TEXT,
             telephone TEXT)''')
    db.commit()

def ajouterContact(nom, prenom, adresse, email, telephone):
    cursor.execute("INSERT INTO contacts (nom, prenom, adresse, email, telephone) VALUES (%s, %s, %s, %s, %s)",
                 (nom, prenom, adresse, email, telephone))
    db.commit()

def ListeContacts():
    cursor.execute("SELECT nom, prenom, email, telephone FROM contacts")
    for row in cursor.fetchall():
        print(row[0].capitalize(), row[1].upper(), "-", row[2].upper(), "-", row[3].upper())

def rechercherContact(nomOUprenom):
    cursor.execute("SELECT nom, prenom, email, telephone FROM contacts WHERE UPPER(nom) = %s OR UPPER(prenom) = %s",
                          (nomOUprenom.upper(), nomOUprenom.upper()))
    for row in cursor.fetchall():
        print(row[0], row[1], "-", row[2], "-", row[3])

def supprimerContact(id_contact, choix=False):
    if choix:
        cursor.execute("DELETE FROM contacts WHERE id=%s", (id_contact,))
    else:
        cursor.execute("UPDATE contacts SET nom=NULL, prenom=NULL, adresse=NULL, email=NULL, telephone=NULL WHERE id=%s", (id_contact,))
    db.commit()

createTable()

while True:
    print("\nMenu:")
    print("1. Ajouter un contact")
    print("2. Afficher tous les contacts")
    print("3. Rechercher un contact avec choix")
    print("4. Supprimer un contact")
    print("5. Quitter")

    choix = input("Entrez votre choix : ")

    if choix == '1':
        nom = input("Entrez le nom du contact : ")
        prenom = input("Entrez le prénom du contact : ")
        adresse = input("Entrez l'adresse du contact : ")
        email = input("Entrez l'e-mail du contact : ")
        telephone = input("Entrez le numéro de téléphone du contact : ")
        ajouterContact(nom, prenom, adresse, email, telephone)
        print("Contact ajouté avec succès.")
    elif choix == '2':
        print("\nListe des contacts :")
        ListeContacts()
    elif choix == '3':
        nomOUprenom = input("Entrez le nom ou prénom du contact à rechercher : ")
        rechercherContact(nomOUprenom)
    elif choix == '4':
        id_contact = int(input("Entrez l'ID du contact à supprimer : "))
        choix_suppression = input("Voulez-vous supprimer définitivement le contact ? (Oui/Non) : ")
        if choix_suppression.lower() == 'oui':
            supprimerContact(id_contact, choix=True)
            print("Contact supprimé définitivement.")
        else:
            supprimerContact(id_contact)
            print("Contact marqué comme supprimé.")
    elif choix == '5':
        print("Merci d'avoir utilisé le programme. Au revoir !")
        break
    else:
        print("Choix invalide. Veuillez réessayer.")

cursor.close()
db.close()
