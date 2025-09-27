import random as r

def creaMazzo():
    mazzo = [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4 + [6] * 4 + [7] * 4 + [8] * 4 + [9] * 4 + [10] * 16
    r.shuffle(mazzo)
    return mazzo

mazzo = creaMazzo()

def pesca_carta():
    global mazzo
    if len(mazzo) == 0:
        print("Mazzo finito, ricreo e mischio un nuovo mazzo")
        mazzo = creaMazzo()
    return mazzo.pop(0)

def risultato(mano):
    totale = sum(mano)
    assi = mano.count(1)
    while assi > 0 and totale + 10 <= 21:
        totale += 10
        assi -= 1
    return totale

def win(m1, m2, puntata, saldo):
    if m1 > 21:
        print("Hai perso!")
        return saldo  # perdita già tolta quando hai scommesso
    elif m2 > 21 or m1 > m2:
        vincita = puntata * 2
        saldo += vincita
        print(f"Hai vinto! Guadagni {vincita}€")
    elif m1 < m2:
        print("Hai perso!")
    else:
        saldo += puntata  # restituisco la puntata
        print("Pareggio!")
    return saldo


# -------------------------------
# INIZIO GIOCO
# -------------------------------

saldo = 1000

print("BLACKJACK")

while saldo > 0:
    print(f"\nSaldo attuale: {saldo}€")
    
    # scelta puntata
    while True:
        try:
            puntata = int(input("Quanto vuoi scommettere? "))
            if puntata > saldo:
                print("Non hai abbastanza soldi!")
            elif puntata <= 0:
                print("Devi puntare almeno 1€")
            else:
                break
        except ValueError:
            print("Inserisci un numero valido!")
    
    saldo -= puntata
    print(f"Hai scommesso {puntata}€, saldo rimanente {saldo}€")

    # mani iniziali
    giocatore = [pesca_carta(), pesca_carta()]
    dealer = [pesca_carta(), pesca_carta()]
    
    while True:
        scoreGiocatore = risultato(giocatore)
        scoreDealer = risultato(dealer)
        
        print("\nDealer:", dealer[0], " ?")
        print("Giocatore:", *giocatore, "=", scoreGiocatore)
        
        if scoreGiocatore > 21:
            saldo = win(scoreGiocatore, scoreDealer, puntata, saldo)
            break
        
        giocata = input("1. Pesca  2. Stai\n").strip()
        
        if giocata == "1":
            giocatore.append(pesca_carta())
        elif giocata == "2":
            while risultato(dealer) < 17:
                dealer.append(pesca_carta())
            
            print("\nDealer:", *dealer, "=", risultato(dealer))
            print("Giocatore:", *giocatore, "=", risultato(giocatore))
            
            saldo = win(risultato(giocatore), risultato(dealer), puntata, saldo)
            break
        else:
            print("Inserisci 1 o 2")

    # fine round
    if saldo <= 0:
        print("\nHai finito i soldi! Game Over")
        break
    else:
        cont = input("\nVuoi continuare? (s/n) ").lower()
        if cont != "s":
            print(f"Esci con {saldo}€")
            break
