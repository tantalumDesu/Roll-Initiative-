import time
from datetime import datetime
from random import randint
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
    log = ""
    for i, (v, k, c) in enumerate(players):
        conditions_str = ", ".join(c) if c else ""
        print(f"{i+1} {v}: ({k}) \x1B[3m{conditions_str}\x1B[0m")
        log += f"{i+1} {v}: ({k}) {conditions_str}\n"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}\n{log}\n"
    with open("initiative_log.txt", "a") as log_file:
        log_file.write(log_entry)
    return log

def saved_encounter(enemies_list):
    prompt = input("Load a saved encounter? y/any: ")
    if prompt == "y":
        with open('saved_encounters.txt', 'r') as f:
            saved = f.read()
            games = eval(saved)
        while True:
            print("\nSaved encounters:")
            for i, game in enumerate(games):
                print(f"{i+1}. {game[0]}")   
            try:
                choose = int(input("\nChoose a saved game: "))
                use = input(f"Use {games[choose-1][0]}? y/n or e(x)it: ")
                if use == "y":
                    enemies = games[choose-1][1]
                    for enemy in enemies:
                        new_enemy = (enemy[0], enemy[1] + randint(1, 20), [])
                        enemies_list.append(new_enemy)
                    print("\nAdded enemies:")
                    for i, (e,k,c) in enumerate(enemies_list):
                        print(f"{i+1}. {e}")
                    return enemies_list
                if use == "n":
                    continue
                elif use=="x":
                    return enemies_list
            except (ValueError, IndexError):
                print("Not a valid choice")
    else:
        return enemies_list

def add_player(players, current_player_index):
    new_combatant=[]
    if players!=[]:
        print("\nCurrent combatants: ")
        enumerateplayers(players)
    while True:
        if new_combatant!=[]:
            print("\nNew combatants: ")
            enumerateplayers(new_combatant)
        name=input("\nEnter new combatant name: ").title()
        if name in [i[0] for i in players] or name in [i[0] for i in new_combatant]:
            print("Use a unique name")              
            continue
        try:
            init=int(input("Inititive: "))   
        except (ValueError, IndexError):
            print("Initiative must be an integer")
            continue
        new_combatant.append((name.title(), init, []))
        print("")
        enumerateplayers(new_combatant)
        while True:
            try:
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
            except ValueError:
                print("Choose 'y', 'n', or 'r")

def add_saved_game(enemies_list):
    players.extend(enemies_list)
    players.sort(key=lambda i:i[1], reverse=True)
    return players

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

def add_condition(players):
    print("\nConditions:\n")
    with open('conditions.txt', 'r') as f:
            saved = f.read()
            condition_list = eval(saved)
    while True:
        for i, conditions in enumerate(condition_list):
            print(f"{i +1}: {conditions}")
        cond_select=int(input("\nSelect a condition: "))
        try:
            use = input(f"Use '{condition_list[cond_select-1]}'? y/n or e(x)it: ")
            if use == "y":
                condition = condition_list[cond_select-1]
                while True:
                    print(f"\nAdd '{condition}' to which player?:")
                    enumerateplayers(players)
                    try:   
                        select=int(input("\nSelect combatant: "))-1
                        if condition in players[select][2]:
                            print(f"\n{players[select][0]} is already '{condition}'\n")
                            continue
                        sure=input(f"\nAdd '{condition}' to {players[select][0]}? y/n: ")
                        if sure=="y":
                            print("")
                            players[select][2].append(condition)
                        elif sure=="n": 
                            cont=input(f"Add '{condition}' to a different player? y/n or e(x)it: ")
                            if cont=="y":
                                continue
                            elif cont=="n":
                                break
                            else:
                                return players
                        another=input(f"Add '{condition}' to another player? y/n: ")
                        if another=="y":
                            if all(condition in player[2] for player in players):
                                print(f"\nAll players are already affected by '{condition}'.")
                                return players
                            else:continue
                        else: return players
                    except(ValueError, IndexError):
                        print("Not a valid selection\n")
            elif use == "n":
                continue
            else: return players
        except (ValueError, IndexError): print("Not a valid choice")           

def remove_condition(players):
    while True:
        players_with_conditions = [player for player in players if player[2]]
        if players_with_conditions:
            print("\nPlayers with conditions:")
            for i, player in enumerate(players_with_conditions):
                conditions_str= ", " .join(player[2])
                print(f"{i + 1}. {player[0]}: \x1B[3m{conditions_str}\x1B[0m")
            try:
                select=int(input("\nSelect combatant: "))-1
                selected_player=players_with_conditions[select]
                conditions_affecting = selected_player[2]
                for i, condition in enumerate(conditions_affecting):
                    print(f"{i+1}. {condition}")
                choose=int(input("\nChoose a condition to remove: "))-1
                sure=input(f"Remove {conditions_affecting[choose]} from {players_with_conditions[select][0]}? y/n: ")
                if sure=="y":
                    selected_player[2].remove(conditions_affecting[choose])
                    return players
                elif sure=="n":
                    cont=input("Remove a different condition? y/n: ")
                    if cont=="y":
                        continue
                    else:
                        return players
            except (ValueError, IndexError): print("Not a valid choice")
        else: 
            print("\nNo combatants are affected by conditions.") 
            return players  
        
def init_order(players, current_player_index):
    animated("3... 2... 1... Fight!")
    round=1
    while True:
        print("\nCombatants:")
        enumerateplayers(players)
        next_player_index = (current_player_index + 1) % len(players)
        if next_player_index == current_player_index:
            animated("Combat is over")
            input("\n\n...")
            return
        animated(f"Round {round}")
        print(f"\n\033[92mCurrent turn: \033[92m{players[current_player_index][0]}\033[0m")
        print(f"\n\033[38;5;208m{players[next_player_index][0]} \033[38;5;208mis next.\033[0m")
        try:
            next = input("\nPress enter for next combatant\nOr, add or remove a (p)layer, add or remove a (c)ondition, or e(x)it: ")
            if next == "":
                round+=1
                current_player_index += 1
                if current_player_index >= len(players):
                    current_player_index = 0
            elif next == "x":
                return
            elif next == "p":
                add_remove=input("(a)dd or (r)emove a player?: ")
                if add_remove == "r":
                    now=players[current_player_index]
                    players=remove_player(players)
                    if current_player_index >= len(players):
                        current_player_index = len(players)-1
                    if now!=players[current_player_index]:
                        round+=1
                    continue
                elif add_remove=="a":
                    players, current_player_index=add_player(players, current_player_index)
                    continue
            elif next=="c":
                choose=input("(a)dd or (r)emove condition?: ")
                if choose=="a":
                    players=add_condition(players)
                elif choose=="r":
                    players=remove_condition(players)
                continue
        except(ValueError):
            print("Not a valid selection\n")
            continue

while True:
    animated("Roll Initiative")
    enemies_list=saved_encounter(enemies_list=[])
    players, current_player_index = add_player(players=[], current_player_index=0)
    players=add_saved_game(enemies_list)
    init_order(players, current_player_index)
