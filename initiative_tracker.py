import time
from datetime import datetime

def animated(animated):
    animated = f"{animated}"
    spin_chars = ['/', '-', '\\', '!']
    print("")
    for i, letter in enumerate(animated):
        spin_char = spin_chars[i % len(spin_chars)]
        print(f"\r\033[31m{animated[:i+1]}\033[31m{spin_char}\033[0m", end="", flush=True)
        time.sleep(0.05)
    print(f"\r\033[31m{animated}\033[31m!\033[0m", end="")
    time.sleep(0.5)
    print("")

def enumerateplayers(players):
    output=""
    for i, (v,k) in enumerate(players):
        print(f"{i+1} {v}: {k}")
        output+=f"{i+1} {v}: {k}\n"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\n{output}\n"
    with open("initiative_log.txt", "a") as log_file:
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
        name=input("\nCombatant name: ").title()
        if name in [i[0] for i in players] or name in [i[0] for i in new_combatant]:
            print("Use a unique name")              
            continue
        try:
            init=int(input("Inititive: "))   
        except (ValueError, IndexError):
            print("Initiative must be an integer")
            continue
        new_combatant.append((name.title(), init))
        print("")
        enumerateplayers(new_combatant)
        while True:
            try:
                if len(new_combatant+players)>=2:
                    another=input("\nAdd another combatant? y/n\nor (r)emove?: ")
                    if another=="y":
                        break
                    elif another=="r":
                        new_combatant=remove_player(new_combatant)
                        if new_combatant!=[]:
                            print("Combatants to add:")
                            enumerateplayers(new_combatant)
                        continue
                    elif another=="n":
                        print("\nCombatants to add:")
                        enumerateplayers(new_combatant)
                        while True:
                            if players!=[]:
                                add=input("\nAdd to combat? y/n?: ")
                            else: add=input("\nBegin combat? y/n?: ")
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
                                    if players!=[]:
                                        return players, current_player_index
                                    else:print(""); enumerateplayers(new_combatant);break
                                else: raise ValueError
                            except ValueError:
                                print("Invalid input. Choose 'y' or 'n'")
                    else: raise ValueError
                else: print("\nAdd another combatant"); break
            except ValueError:
                print("Choose 'y', 'n', or 'r")

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
    animated("    Fight!")
    print("\nCombatants:")
    enumerateplayers(players)
    round=1
    while True:
        next_player_index = (current_player_index + 1) % len(players)
        if next_player_index == current_player_index:
            animated("Combat is over")
            return
        animated(f"Round {round}")
        print(f"\n\033[92mCurrent turn: \033[92m{players[current_player_index][0]}\033[0m")
        print(f"\n\033[38;5;208m{players[next_player_index][0]} \033[38;5;208mis next.\033[0m")
        try:
            next = input("\nPress enter for next combatant\nOr (r)emove, (a)dd or e(x)it: ")
            if next == "":
                round+=1
                current_player_index += 1
                if current_player_index >= len(players):
                    current_player_index = 0
            elif next == "x":
                return
            elif next == "r":
                now=players[current_player_index]
                players=remove_player(players)
                if current_player_index >= len(players):
                    current_player_index = len(players)-1
                if now!=players[current_player_index]:
                    round+=1
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
    animated("Roll Initiative")
    players=[]
    current_player_index=0
    players, current_player_index = add_player(players, current_player_index)
    init_order(players, current_player_index)
