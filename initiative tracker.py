import time
from datetime import datetime

def title():
    title = "Roll Initiative"
    spin_chars = ['/', '-', '\\', '!']
    print("")
    for i, letter in enumerate(title):
        spin_char = spin_chars[i % len(spin_chars)]
        print(f"\r{title[:i+1]}{spin_char}", end="", flush=True)
        time.sleep(0.05)
    for i in range(4):
        spin_char = spin_chars[i % len(spin_chars)]
        print(f"\r{title}{spin_char}", end="")
        time.sleep(0.05)
    print("")


def enumerateplayers(players):
    output=""
    for i, (v,k) in enumerate(players):
        print(f"{i+1} {v}: {k}")
        output+=f"{i+1} {v}: {k}\n"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\n{output}\n"
    with open("initiative log.txt", "a") as log_file:
        log_file.write(log_entry)
    return output

def add_player(players, current_player_index):
    new_combatant=[]
    current_player_index=int(current_player_index)
    if players!=[]:
        print("\nCurrent combatants: ")
        enumerateplayers(players)
    while True:
        if new_combatant!=[]:
            print("\nNew combatants: ")
            enumerateplayers(new_combatant)
        name=input("\nCombatant name: ").capitalize()
        if name in [i[0] for i in players] or name in [i[0] for i in new_combatant]:
            print("Use a unique name")              
            continue
        try:
            init=int(input("Inititive: "))   
        except (ValueError, IndexError):
            print("Initiative must be a number")
            continue
        new_combatant.append((name.capitalize(), init))
        while True:
            try:
                another=input("\nAdd another? y/n: ")
                if another=="y":
                    break
                elif another=="n":
                    print("")
                    if len(players+new_combatant)<2:
                        print("Not enough combatants!")
                        continue
                    print("Combatants to add:")
                    for i, (v,k) in enumerate(new_combatant):
                        print(f"{i+1} {v}: {k}")
                    while True:
                        add=input(f"\nAdd to combatant list? y/n (r)emove: ")
                        try:
                            if add=="y":
                                print("")
                                if players!=[]:
                                    now=players[current_player_index]
                                    players.extend(new_combatant)
                                    players.sort(key=lambda i:i[1], reverse=True)
                                    current_player_index=players.index(now)
                                    return players, current_player_index
                                else: 
                                    players.extend(new_combatant)
                                    players.sort(key=lambda i:i[1], reverse=True)
                                    return players, current_player_index
                            elif add=="n":
                                return players, current_player_index
                            elif add=="r":
                                new_combatant=remove_player(new_combatant)
                                print("Combatants to add:")
                                enumerateplayers(new_combatant)
                                continue
                            else: raise ValueError
                        except ValueError:
                            print("Invalid input. Choose 'y', 'n', or 'r'.")
                else: raise ValueError
            except ValueError:
                print("Choose 'y' or 'n'")

def remove_player(players):
    print("\nCombatants to remove:")
    enumerateplayers(players)
    while True:
        try:   
            remove=int(input("\nSelect combatant to remove: "))-1
            sure=input(f"Remove {players[remove][0]}? y/n: ")
            if sure=="y":
                print("")
                players.pop(remove)
                return players
            else: print(""); return players
        except(ValueError, IndexError):
            print("Not a valid selection\n")

def init_order(players, current_player_index):
    print("\nCombatants:")
    enumerateplayers(players)
    while True:
        if current_player_index >= len(players):
            current_player_index = len(players)-1
        next_player_index = (current_player_index + 1) % len(players)
        if next_player_index == current_player_index:
            print("\nCombat is over!")
            return
        print(f"\nCurrent turn: {players[current_player_index][0]}")
        print(f"\nNext player: {players[next_player_index][0]}")
        try:
            next = input("\nPress enter for next combatant\nOr (r)emove, (a)dd or e(x)it: ")
            if next == "":
                current_player_index += 1
                if current_player_index >= len(players):
                    current_player_index = 0
            elif next == "x":
                return
            elif next == "r":
                players=remove_player(players)
                print("\nCombatants:")
                enumerateplayers(players)
                continue
            elif next=="a":
                players, current_player_index=add_player(players, current_player_index)
                print("\nCombatants:")
                enumerateplayers(players)
                continue
        except(ValueError):
            print("Not a valid selection\n")
            continue

while True:
    title()
    players=[]
    current_player_index=0
    players, current_player_index = add_player(players, current_player_index)
    init_order(players, current_player_index)