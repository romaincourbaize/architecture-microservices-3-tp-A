# Travaux réalisés par Jodie Monterde & Romain Courbaize

import socket
import threading

# Etape 1
# A quel moment la socket côté serveur est-elle bloquante ?
# Elle est bloquante le temps d'attendre le message

# Que se passe-t-il si le client se connecte avant que le serveur ne soit prêt ?
# Une erreur apparait car le serveur n'a pas ouvert ses ports, la connexion est refusée

# Quelle est la différence entre bind() et listen() ?
# Bind associe la prise à une adresse et un port
# Listen démarre l'écoute des connexions entrantes sur le socket

# Etape 2
# Pourquoi faut-il une boucle dans le serveur ?
# Il s'arrête au premier message qu'il reçoit sinon
# Que se passe-t-il si on oublie de tester msg == "fin" ?
# La connexion ne se ferme jamais
# Est-ce que le serveur peut envoyer plusieurs réponses d’affilée ?
# Non, puisqu'il attend le message du client avant de lui-même envoyer un message.

# Création d'une socket côté serveur
#serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serveur.bind(("", 63000))

#serveur.listen(1)
#conn, addr = serveur.accept()

#while True:
#    message = conn.recv(1024).decode()
#    conn.send(message.encode())
#    print("Message : ", message)
#    if message == "fin":
#        break

#serveur.close()

# Etape 3
#serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serveur.bind(("", 63000))

#serveur.listen(1)
#while True:
#    conn, addr = serveur.accept()
#    print("Connexion de", addr)
#    while True:
#        msg = conn.recv(1024).decode()
#        print("Message : ", msg)
#        conn.send(msg.encode())
#        if msg == "fin":
#            break
#    conn.close()

# Le serveur peut-il rester actif après une déconnexion client ?
# Que faut-il modifier pour accepter plusieurs clients à la suite ?
# Oui, d'ou le while True. Il reste ouvert après la fermeture de la connexion avec le client.
# Peut-on imaginer accepter des clients en parallèle ?
# On peut imaginer de multithreader la phase de connexion.

# Etape 4
#serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serveur.bind(("", 63000))

#serveur.listen(1)
#while True:
#    conn, addr = serveur.accept()
#    print("Connexion de", addr)
#    while True:
#        msg = conn.recv(1024).decode()
#        print("Client : ", msg)
#        if msg == "fin":
#            conn.send("fin".encode())
#            break
#        reponse = input("Répondre > ")
#        if reponse == "fin":
#            conn.send("fin".encode())
#            break
#        conn.send(reponse.encode())
#    conn.close()

# Comment s’assurer que les deux côtés ne parlent pas en même temps ?
# Chaque côté attend la réponse de l'autre avant de permettre l'envoi d'un nouveau message
# Peut-on rendre cet échange non bloquant ? Comment ?
# Un thread qui écoute et un qui envoie.
# Quelle est la meilleure façon de quitter proprement la communication ?
# Utiliser un message de fin qui est géré par le serveur "fin" et qui ferme la connexion

# Etape 5
#serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serveur.bind(("", 63000))

#serveur.listen(1)
#while True:
#    conn, addr = serveur.accept()
#    print("Connexion de", addr)
#    while True:
#        msg = conn.recv(1024).decode()
#        print("Client : ", msg)
#        if msg == "fin":
#            conn.send("fin".encode())
#            break
#        print("Expression reçue:", msg)
#        # Évaluation sécurisée
#        try:
#            result = eval(msg)
#            conn.send(str(result).encode())
#        except Exception as e:
#            conn.send(f"Erreur: {e}".encode())
#    conn.close()

# Quels sont les risques d’utiliser eval() ? (souvenirs de FONDADEV)
# eval présente un risque d'injection de code, tous les appels de fonction sont executées sans vérification, un utilisateur mal intentionné peut casser l'application
# Comment renvoyer une erreur sans faire planter le serveur ?
# Il faut utiliser un try/catch, si le bloc dans le try "plante", on passe dans le except sans executer la suite du code et donc sans risquer un planton

# Etape 6
#serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serveur.bind(("", 63000))

#serveur.listen(1)
#while True:
#    conn, addr = serveur.accept()
#    print("Connexion de", addr)
#    while True:
#        msg = conn.recv(1024).decode()
#        # Découper la commande en parties
#        parts = msg.split(" ", 1)
#        commande = parts[0]
#        contenu = parts[1] if len(parts) > 1 else ""
#        if commande == "/me":
#            conn.send(f"* {conn} {contenu}".encode())
#            print(f"* {conn} {contenu}")
#        elif commande == "/all":
#            conn.send(f"[{conn}] {contenu}".encode())
#            print(f"[{conn}] {contenu}")
#        elif commande == "/bye":
#            conn.send("A bientot {conn} !".encode())
#            print("A bientot {conn} !")
#            conn.send("fin".encode()) # Message pour prévenir le client que le #serveur ferme la connexion
#            break
#        else:
#            conn.send("Commande inconnue !".encode())
#    conn.close()

# Pourquoi structurer les messages avec /commande ?
# On s'approche d'une API REST, cela permet de codifier
# Comment distinguer facilement les types de messages côté serveur ?
# En utilisant des /commande, on a une syntaxe facilement identifiable et donc facilement exploitable.

# Etape 7
#def gerer_client(conn, addr):
#    while True:
#        # On lit le message envoyé par le client
#        msg = conn.recv(1024).decode()
#        if msg == "fin":
#            break # Si le message est "fin", on ferme la 
#        # On renvoie le même message (echo)
#        conn.send(msg.encode())
#        # Une fois terminé, on ferme la connexion avec ce client
#    conn.close()

#serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serveur.bind(("", 63000))
#serveur.listen(1)
## Boucle principale du serveur : accepte les connexions
#while True:
#    conn, addr = serveur.accept()
#    # Pour chaque nouveau client, on crée un thread dédié
#    threading.Thread(target=gerer_client, args=(conn,addr)).start()

# Que se passe-t-il si deux clients envoient des messages en même temps ?
# Ils sont chacun dans un thread unique. Si l'on écrivait côté serveur cela poserait des problèmes d'accès concurent.
# Peut-on garder un état partagé entre clients ? Est-ce souhaitable ?
# Si l'on écrivait côté serveur, cela poserait des problèmes d'accès concurent, cela n'est donc pas souhaitable.
# Que faut-il pour aller plus loin vers une vraie messagerie ?
# Il faudrait utiliser des mutex côté serveur par exemple pour bloquer l'accès à un espace partagé (stockage des messages).

# Etape 8
def gerer_client(conn, addr):
    global messages
    while True:
        # On lit le message envoyé par le client
        msg = conn.recv(1024).decode()
        if msg == "fin":
            break # Si le message est "fin", on ferme la
        elif msg == "/all":
            conn.send(messages.encode())
        else:
            with lock:
                messages += msg + "\n"
                print("Ajout sécurisé")
        # On renvoie le même message (echo)
        conn.send(msg.encode())
        # Une fois terminé, on ferme la connexion avec ce client
    conn.close()

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
lock = threading.Lock()
messages = ""
# Boucle principale du serveur : accepte les connexions
while True:
    conn, addr = serveur.accept()
    # Pour chaque nouveau client, on crée un thread dédié
    threading.Thread(target=gerer_client, args=(conn,addr)).start()

# Pourquoi faut-il protéger certaines sections du code ?
# Pour éviter des corruptions de données lors de l'écriture dans les messages si plusieurs clients écrivent en même temps. 
# Que risque-t-on si deux clients modifient une même ressource simultanément ?
# Les 2 messages se mélangent, que l'un des 2 ne soient pas envoyés, ...
