import random as r

# Function to create a new deck
def create_deck():
    # Deck: numbers 1–9 have 4 copies each, 10 has 16 copies (representing 10, J, Q, K of each suit)
    deck = [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4 + [6] * 4 + [7] * 4 + [8] * 4 + [9] * 4 + [10] * 16
    r.shuffle(deck)  # Shuffle the deck
    return deck

# Initialize deck
deck = create_deck()

# Function to draw a card
def draw_card():
    global deck
    if len(deck) == 0:  # If the deck is empty, recreate and shuffle it
        print("Deck is empty, creating and shuffling a new one")
        deck = create_deck()
    return deck.pop(0)  # Remove and return the top card

# Function to calculate the hand total
def hand_value(hand):
    total = sum(hand)
    aces = hand.count(1)  # Aces can count as 1 or 11
    # If possible, turn Ace from 1 into 11 (but not busting over 21)
    while aces > 0 and total + 10 <= 21:
        total += 10
        aces -= 1
    return total

# Function to determine winner and update balance
def check_winner(player_score, dealer_score, bet, balance):
    if player_score > 21:  # Player bust
        print("You lost!")
        return balance  # Bet already deducted when placing it
    elif dealer_score > 21 or player_score > dealer_score:  # Dealer busts or player higher
        winnings = bet * 2
        balance += winnings
        print(f"You won! You gain {winnings}€")
    elif player_score < dealer_score:  # Dealer higher
        print("You lost!")
    else:  # Tie
        balance += bet  # Return the bet
        print("It's a tie!")
    return balance


balance = 1000  # Starting money

print("BLACKJACK")

while balance > 0:
    print(f"\nCurrent balance: {balance}€")
    
    # Player chooses bet
    while True:
        try:
            bet = int(input("How much do you want to bet? "))
            if bet > balance:
                print("You don’t have enough money!")
            elif bet <= 0:
                print("You must bet at least 1€")
            else:
                break
        except ValueError:
            print("Enter a valid number!")
    
    # Deduct bet from balance
    balance -= bet
    print(f"You bet {bet}€, remaining balance {balance}€")

    # Initial hands
    player = [draw_card(), draw_card()]
    dealer = [draw_card(), draw_card()]
    
    while True:
        player_score = hand_value(player)
        dealer_score = hand_value(dealer)
        
        # Show dealer's first card only
        print("\nDealer:", dealer[0], " ?")
        print("Player:", *player, "=", player_score)
        
        # Check if player already busted
        if player_score > 21:
            balance = check_winner(player_score, dealer_score, bet, balance)
            break
        
        # Player’s choice
        move = input("1. Hit  2. Stand\n").strip()
        
        if move == "1":  # Hit
            player.append(draw_card())
        elif move == "2":  # Stand
            # Dealer must draw until reaching 17 or more
            while hand_value(dealer) < 17:
                dealer.append(draw_card())
            
            # Show final hands
            print("\nDealer:", *dealer, "=", hand_value(dealer))
            print("Player:", *player, "=", hand_value(player))
            
            balance = check_winner(hand_value(player), hand_value(dealer), bet, balance)
            break
        else:
            print("Enter 1 or 2")

    # End of round
    if balance <= 0:
        print("\nYou’re out of money! Game Over")
        break
    else:
        cont = input("\nDo you want to continue? (y/n) ").lower()
        if cont != "y":
            print(f"You leave with {balance}€")
            break
