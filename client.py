import socket

# Création d'une socket côté client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.16.20.250", 63000))

while True:
    inp = input("Client > ") 
    client.send(inp.encode())
    msg = client.recv(1024).decode()
    if msg == "fin":
        print("Fermeture de la connexion")
        break
    print("Serveur > ", msg)

client.close()
