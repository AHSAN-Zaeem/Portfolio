import datetime


class ListeTache:

    '''Classe qui paramètre une liste de tâches à faire'''

    def __init__(self):
        self.taches = []
        self.prochain_id = 1  # compteur pour garantir des id uniques

    def int_input(self, text):

        """Fonction qui permet de transformer en entier toute entrée de la
        fonction input en étant sûr de ne pas causer d'erreur"""

        while True:
            entree = input(text)
            try:
                return int(entree)
            except ValueError:
                print("Erreur : vous devez entrer un nombre entier.")

    def priorite_input(self, text="Quel est le rang de priorité de cette tâche ? (1 ou plus) "):

        """Demande une priorité valide (entier >= 1)"""

        prio = self.int_input(text)
        while prio < 1:
            prio = self.int_input("La priorité doit être de 1 ou plus : ")
        return prio

    def date_input(self):

        """Fonction qui permet d'obtenir une date sous forme de tuple (jour, mois, année)"""

        while True:
            jour = self.int_input("Quel jour est-on ? (JJ) ")
            mois = self.int_input("Quel mois est-on ? (MM) ")
            annee = self.int_input("De quelle année ? (AAAA) ")
            try:
                # datetime vérifie tout, années bissextiles comprises
                datetime.date(annee, mois, jour)
                return jour, mois, annee
            except ValueError:
                print("Date invalide, recommencez s'il vous plaît")

    def ajouter_tache(self):

        """Fonction qui permet d'ajouter une tâche à la liste"""

        titre = input("Quel est le titre de votre tâche ? ").strip()
        while not titre:
            titre = input("Le titre ne peut pas être vide : ").strip()

        prio = self.priorite_input()
        date_c = self.date_input()

        self.taches.append({
            'titre': titre,
            'priorite': prio,
            'date_crea': date_c,
            'id': self.prochain_id,
        })
        self.prochain_id += 1

    def afficher_taches(self, liste=None, tri_par=None, croissant=True):
        """Affiche les tâches avec tri possible, sans modifier la liste d'origine.

        Le paramètre liste est la liste de tâches
        à afficher (None si on veut toutes les tâches)

        Le paramètre tri_par signifie le type de tri utilisé,
        'priorite' ou 'date' (None pour aucun tri)

        Le paramètre croissant indique si le tri est dans l'ordre croissant
        (True, par défaut) ou décroissant (False)"""

        if liste is None:
            liste = self.taches

        if not liste:
            print("Aucune tâche à afficher.")
            return

        if tri_par == 'priorite':
            liste = sorted(liste, key=lambda t: t['priorite'], reverse=not croissant)
        elif tri_par == 'date':
            # (année, mois, jour) pour comparer chronologiquement
            liste = sorted(liste, key=lambda t: t['date_crea'][::-1], reverse=not croissant)

        for i, t in enumerate(liste, start=1):
            jour, mois, annee = t['date_crea']
            print(f"{i}. {t['titre']}, priorité: {t['priorite']}, "
                  f"Créée le: {jour:02d}/{mois:02d}/{annee}")

    def trouve_tache(self):

        """Fonction qui permet de trouver une tâche spécifique dans la liste de tâches"""

        char = input("Quel est le titre de la tâche ? ")
        correspond = [t for t in self.taches if char.lower() in t["titre"].lower()]

        if not correspond:
            print(f"Aucune tâche trouvée contenant '{char}'")
            return None

        if len(correspond) == 1:
            return correspond[0]

        print("Plusieurs tâches trouvées : ")
        self.afficher_taches(liste=correspond)
        choix = self.int_input("Numéro de la tâche choisie : ")
        while not 1 <= choix <= len(correspond):
            choix = self.int_input(f"Entrez un numéro entre 1 et {len(correspond)} : ")
        return correspond[choix - 1]

    def modifier_tache(self):

        """Fonction qui permet de modifier les tâches de la liste"""

        tache = self.trouve_tache()
        if tache is None:
            return

        proprietes = {1: 'titre', 2: 'priorite'}
        print("Propriétés modifiables : ")
        for num, nom in proprietes.items():
            print(f"{num}. {nom}")

        choix = self.int_input("Numéro de la propriété à modifier : ")
        while choix not in proprietes:
            choix = self.int_input("Le numéro de la propriété est 1 ou 2 : ")

        if proprietes[choix] == 'priorite':
            tache['priorite'] = self.priorite_input("Nouvelle priorité : ")
        else:
            nouveau = input("Nouveau titre : ").strip()
            while not nouveau:
                nouveau = input("Le titre ne peut pas être vide : ").strip()
            tache['titre'] = nouveau

    def fin_tache(self):

        """Fonction permettant de déclarer une tâche finie, et donc de la supprimer de la liste"""

        tache = self.trouve_tache()
        if tache is None:
            return

        self.taches = [t for t in self.taches if t['id'] != tache['id']]
        print(f"La tâche '{tache['titre']}' a été supprimée avec succès.")