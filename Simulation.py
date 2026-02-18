from Card import Card
import config

class Simulation:
    def __init__(self, base=10, pot=100):
        self.played = 0
        self.passes = 0
        self.loses = 0
        self.wins = 0
        
        self.win_value = 0
        self.lose_value = 0
        
        self.initial = base
        self.base = base
        self.pot = pot
        self.collected = { "HEARTS": [], "SPADES": [], "CLUBS": [], "DIAMONDS": [] }

    def setBase(self, base):
        self.intitial = base
        self.base = base

    def setPot(self, pot):
        self.pot = pot

    def getBase(self):
        return self.base

    def nextCard(self):
        random_card = Card()
        value, suit = random_card.getValue(), random_card.getSuit()
        
        while value in self.collected[suit]:
            random_card = Card()
            value, suit = random_card.getValue(), random_card.getSuit()

        # random_card.displayCard()
        self.storeCard(random_card)
        return random_card

    def storeCard(self, card):
        self.collected[card.getSuit()].append(card.getValue())

    def calcOdds(self, first, second):
        
        value_first = first.getValue()
        value_second = second.getValue()
    
        # count all remaining (uncollected) cards
        all_remaining = []
        for suit in config.SUITS:
            for value in range(config.VAL_START, config.VAL_END + 1):
                if value not in self.collected[suit]:
                    all_remaining.append(value)
    
        total_remaining = len(all_remaining)
    
        if value_first == value_second:
            value = value_first
            greater = sum(1 for v in all_remaining if v > value)
            lower = sum(1 for v in all_remaining if v < value)
    
            if greater >= lower:
                return "GREATER", round(greater / total_remaining, 2)
            else:
                return "LOWER", round(lower / total_remaining, 2)
    
        else:
            low, high = min(value_first, value_second), max(value_first, value_second)
            in_between = sum(1 for v in all_remaining if low < v < high)
    
            return "NIL", round(in_between / total_remaining, 2)

    def displayCollection(self):
        for suit in self.collected:
            print(f"{suit}: {self.collected[suit]}")

    def gameFinish(self):
        # print(f"\n{"="*30} \nBalance: ${self.base}")
        if self.base <= 0:
            # print("You have lost the game!")
            return True
            
        total = 0
        for suits in self.collected:
            if len(self.collected[suits]) > 10:
                total += 1

        return total == 4

    def getStats(self):
        if self.played == 0:
            return 0, 0, 0, 0, 0

        return self.wins, self.loses, self.passes, self.win_value, self.lose_value
        
    def startPlayer(self):
        while not(s.gameFinish()):
            first = s.nextCard()
            second = s.nextCard()

            value_first = first.getValue()
            value_second = second.getValue()
        
            print(f"First card: {first.displayCard()}")
            print(f"Second card: {second.displayCard()}")
        
            c, p = s.calcOdds(first, second)
            p = round(p * 100, 2)
            if c == "NIL":
                print(f"*{p}% chance of winning")
            else:
                print(f"{c}: {p}% chance of winning")

            print("\n")
            
            choice = "c"
            if value_first == value_second:
                print("\na) Higher\nb) Lower")
                choice = input("Enter choice: ")
                choice = choice.lower()
                
                print("Choice:", choice)
                while choice != "a" and choice != "b":
                    print("Invalid option!")
                    choice = input("Enter choice: ")
                    print("Choice:", choice)
                
                
            bet = int(input("Place bet (-1 to pass): "))
            while bet > self.base // 2 or bet > self.pot:
                print("Bet size is too large!")
                bet = int(input("Place bet (-1 to pass): "))

            if bet == -1:
                self.passes += 1
                continue

            self.played += 1

            result = s.nextCard()
            result_val = result.getValue()
            print(f"{"-"*5} Your card: {result.displayCard()} {"-"*5}")
            
            choice = choice.lower()
            win = False
            tiang = False
            if choice == "c":
                # in between
                if result_val > min(value_first, value_second) and result_val < max(value_first, value_second):
                    # win
                    win = True
                elif result_val == value_first or result_val == value_second:
                    tiang = True
            elif choice == "a":
                # higher
                if result_val > value_first:
                    # win
                    win = True
                elif result_val == value_first or result_val == value_second:
                    tiang = True
            elif choice == "b":
                # lower
                if result_val < value_first:
                    # win
                    win = True
                elif result_val == value_first or result_val == value_second:
                    tiang = True

            if win:
                print(f"WIN! +${bet}")
                self.base += bet
                self.wins += 1
            else:
                if tiang:
                    print("TIANG")
                    print(f"LOSE! -${bet * 2}")
                    self.base -= bet * 2
                else:
                    print(f"LOSE! -${bet}")
                    self.base -= bet
                    

            if self.base < 5:
                print(f"Current Balance: ${self.base}")
                top_up = input("Top up? Y: ")
                if top_up.upper() == "Y":
                    amt = int(input("Top up amount: "))
                    self.base += amt
                else:
                    print("="*30)
                    print("Game over!")
                    print(f"Initial Balance: ${self.initial}")
                    print(f"Final Balance: ${self.base}")
                    
                    profit = self.base - self.initial
                    print(f"Profit: {"+" if profit >= 0 else "-"}${abs(profit)}")
                    print("="*30)
                    break

    def startComputer(self, skip_threshold=0.4):
        while not self.gameFinish():
            first = self.nextCard()
            second = self.nextCard()
    
            value_first = first.getValue()
            value_second = second.getValue()
    
            # print(f"First card: {first.displayCard()}")
            # print(f"Second card: {second.displayCard()}")
    
            c, p = self.calcOdds(first, second)
            p_display = round(p * 100, 2)
    
            # if c == "NIL":
            #     print(f"*{p_display}% chance of winning")
            # else:
            #     print(f"{c}: {p_display}% chance of winning")
    
            # --- Computer Decision ---
    
            if p < skip_threshold:
                # print("Computer passes.\n")
                self.passes += 1
                continue

            self.played += 1
    
            choice = "c"
            if value_first == value_second:
                choice = "a" if c == "GREATER" else "b"
                # print(f"Computer chooses: {'Higher' if choice == 'a' else 'Lower'}")
    
            max_allowed = min(self.base // 2, self.pot) - 1
            bet = max(1, int(max_allowed * p))  # scale bet by probability
            # print(f"Computer bets: ${bet}")
    
            result = self.nextCard()
            result_val = result.getValue()
            # print(f"-----  Your card: {result.displayCard()} -----")
    
            win = False
            tiang = False
            if choice == "c":
                if min(value_first, value_second) < result_val < max(value_first, value_second):
                    win = True
                elif result_val == value_first or result_val == value_second:
                    tiang = True
            elif choice == "a":
                if result_val > value_first:
                    win = True
                elif result_val == value_first:
                    tiang = True
            elif choice == "b":
                if result_val < value_first:
                    win = True
                elif result_val == value_first:
                    tiang = True
    
            if win:
                # print(f"WIN! +${bet}")
                self.base += bet
                self.wins += 1
                self.win_value += bet
            else:
                self.loses += 1
                if tiang:
                    # print(f"TIANG! LOSE! -${bet * 2}")
                    self.base -= bet * 2
                    self.lose_value += bet * 2
                else:
                    # print(f"LOSE! -${bet}")
                    self.base -= bet
                    self.lose_value += bet
   
            # print(f"Current Balance: ${self.base}\n")
    
        # print("=" * 30)
        # print("Game complete.")
        # print(f"Initial Balance: ${self.initial}")
        # print(f"Final Balance: ${self.base}")
        # profit = self.base - self.initial
        # print(f"Profit: {'+' if profit >= 0 else '-'}${abs(profit)}")
        # print("=" * 30)