import sys

REFERENCE_FREQUENCIES = {
    'a': 8.13, 'b': 0.93, 'c': 3.15, 'd': 3.55, 'e': 17.32,
    'f': 1.06, 'g': 0.97, 'h': 0.74, 'i': 7.31, 'j': 0.31,
    'k': 0.05, 'l': 5.69, 'm': 2.89, 'n': 7.12, 'o': 5.28,
    'p': 3.02, 'q': 0.99, 'r': 6.43, 's': 7.91, 't': 7.11,
    'u': 6.05, 'v': 1.83, 'w': 0.04, 'x': 0.42, 'y': 0.19,
    'z': 0.21
}

def cypher_encoder(text, shift):
    resultat = ""
    if shift > 26:
        shift = shift % 26
    for lettre in text:
        if lettre.isalpha():
            resultat += chr((ord(lettre) + shift))
        else:
            resultat += lettre
    return resultat

def cypher_decoder(text, shift):
    if shift > 26:
        shift = shift % 26
    resultat = ""
    for lettre in text:
        if lettre.isalpha():
            resultat += chr((ord(lettre) - shift))
        else:
            resultat += lettre
    return resultat

def calculate_frequencies(text):
    text = text.lower()
    total_lettres = len(text)
    # Initialisation du tableau de fréquences
    frequences = {}
    for i in range(97,123):
        lettre = chr(i)
        frequences[lettre] = 0

    # Comptage des lettres du texte et ajout au tableau de fréquence
    for lettre in text:
        if lettre.isalpha():
            frequences[lettre] += 1

    # Calcule de la fréquence de chaque lettre
    for lettre in frequences:
        if total_lettres > 0:
            frequences[lettre] = (frequences[lettre]/total_lettres) * 100
        else:
            frequences[lettre] = 0
    return frequences

def chi_squared_statistic(observed_frequencies, reference_frequencies):
    resultat = 0
    for lettre in reference_frequencies:
        freq_attendu = reference_frequencies[lettre]
        if freq_attendu > 0:
            freq_observe = observed_frequencies.get(lettre, 0)
            resultat += ((freq_observe - freq_attendu)**2) / freq_attendu
    return resultat

def auto_decrypt(ciphertext):
    meilleur_texte = ""
    meilleure_decalage = 0
    meilleur_chi_squared = float("inf")

    for decalage in range(1,26):
        texte_decode = cypher_decoder(ciphertext,decalage)
        frequences = calculate_frequencies(texte_decode)
        chi_squared = chi_squared_statistic(frequences, REFERENCE_FREQUENCIES)

        if chi_squared < meilleur_chi_squared:
            meilleur_chi_squared = chi_squared
            meilleur_texte = texte_decode
            meilleure_decalage = decalage
    return meilleur_texte, meilleure_decalage

if len(sys.argv) == 3:  # Mode encodage
    texte = sys.argv[1]
    decalage = int(sys.argv[2])
    print("Texte encodé :", cypher_encoder(texte, decalage))

elif len(sys.argv) == 2:  # Mode décryptage automatique
    texte_chiffre = sys.argv[1]
    texte_dechiffre, decalage_trouve = auto_decrypt(texte_chiffre)
    print(f"Texte déchiffré : {texte_dechiffre} (Décalage trouvé : {decalage_trouve})")

else:  # Mode interactif
    texte = input("Entrez un texte à encoder : ")
    decalage = int(input("Entrez un décalage : "))
    texte_encode = cypher_encoder(texte, decalage)
    print("Texte encodé :", texte_encode)
    print("Texte décodé :", cypher_decoder(texte_encode, decalage))

