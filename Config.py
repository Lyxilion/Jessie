print("Quels credentials voulez-vous changer ? :")
print("   - 1. Twitter")

choice = input("Numéro : ")

if int(choice) == 1 :
    print("Vous avez choisi Twitter.")
    consKey = input("Consumer Key : ")
    consSecret = input("Consumer Secret : ")
    tokenKey = input("Access Token Key : ")
    tokenSecret = input("Access Token Secret : ")
    fichier = open("Data/credentials.txt", "w")
    fichier.write(consKey+"\n"+consSecret+"\n"+tokenKey+"\n"+tokenSecret)
    fichier.close()
    print("Les credentials ont bien été modifieés.")
else :
    print("Error")