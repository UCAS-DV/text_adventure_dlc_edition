from helper_funcs import inq_select
from inspect_character import get_char_stats
from game_assets import *
from dialogue_reader import read_dialogue
from dialogue_reader import read_description
from save_load import player_data
from battle import battle
from level_up import level_up
from save_load import save_dlc

dlc_locations = [
    {
        "name": "North Dakotan Capitol",
        "mini_locations": ["Train", "Town Square", "Department of EMUSA Affairs", "Slums", "Palace"],
        'mini_local_desc': ['dlc_dialogue/north_dakota/train.txt',
                            'dlc_dialogue/north_dakota/nd_town_square.txt',
                            'dlc_dialogue/north_dakota/nd_dea.txt',
                            '',
                            ''],
        "intro": 'dlc_dialogue/north_dakota/north_dakota_intro.txt',
        "item": {'item': northdakotium, 'position': 2, 'collected': False},
        "boss": {'boss_encounter': king_fight, 'position': 4, 'defeated': False},
        "ally": prince_ally,
        "encounter": {'fight': nd_encounter, 'position': 3, 'defeated': False}
    },
    {
        "name": "New Rome",
        "mini_locations": ["New Rome Sign", "Colosseum", "Senate", "Studio", "Dizzy Land"],
        'mini_local_desc': ['dlc_dialogue/new_rome/sign.txt',
                            'dlc_dialogue/north_dakota/nd_town_square.txt',
                            '',
                            '',
                            ''],
        "intro": 'dlc_dialogue/new_rome/nr_intro.txt',
        "item": {'item': film_roll, 'position': 3, 'collected': False},
        "boss": {'boss_encounter': srjc_fight, 'position': 4, 'defeated': False},
        "ally": prince_ally,
        "encounter": {'fight': nd_encounter, 'position': 2, 'defeated': False}
    },
]

def dlc_explore(location):
    options = location['mini_locations'] + ['Back']

    selection = inq_select('Where do you want to go?', *options) - 1

    if selection == len(options) - 1:
        return False
    
    if selection == location['item']['position'] and not location['item']['collected'] and location['item']['item'] not in player_data['inventory']:
        read_dialogue(location['mini_local_desc'][selection])
        input(f"You now have {location['item']['item']}!")
        player_data['inventory'].append(location['item']['item'])
        location['item']['collected'] = True
        return False
    elif selection == location['item']['position'] and location['item']['collected']:
        return False

    if selection == location['boss']['position'] and not location['boss']['defeated']:

        if inq_select("You are entering a boss battle. Do you wish to continue?", "No", "Yes") == 2:
            boss_fight = location['boss']['boss_encounter']
            result, empty_list = battle(party, boss_fight.enemies, boss_fight.opening, boss_fight.closing, player_data['inventory'], boss_fight.special_function)

            if result:
                level_up(party + benched_allies, inq_select("What do you want to level up?", "Durability", "Bravery", "Strength", "Recovery"), 1)
                input(f"{location['ally'].name} has joined our party!")
                input(f"You can access {location['ally'].name} by changing your party composition!")
                benched_allies.append(location['ally'])
                location['boss']['defeated'] = True

            return result
        else:
            return False

    if selection == location['encounter']['position'] and not location['encounter']['defeated']:

        if inq_select("You are entering an encounter. Do you wish to continue?", "No", "Yes") == 2:
            fight = location['encounter']['fight']
            result, empty_list = battle(party, fight.enemies, fight.opening, fight.closing, player_data['inventory'])
            if result:
                level_up(party + benched_allies, inq_select("What do you want to level up?", "Durability", "Bravery", "Strength", "Recovery"), 0.5)
                location['encounter']['defeated'] = True
            return False
        else:
            return False
    
    read_dialogue(location['mini_local_desc'][selection])

def menu(location, index):

    global party

    defeated_boss = False

    save_dlc()

    read_dialogue(location['intro'])

    while True:

        if not defeated_boss:
            match inq_select(f"What do you want to do in {location['name']}?", "Explore", "Inspect Team", 'Inventory', "Save", "Exit To Main Menu"):
                case 1:
                    defeated_boss = dlc_explore(location)
                case 2:
                    match inq_select(f"Stats: \nDurability: {player_data['durability']} \nBravery: {player_data['bravery']} \nStrength: {player_data['strength']} \nRecovery: {player_data['recovery']} \nWhat do you want to do?", "Inspect Party Members", "Change Party Composition", "Back"):
                        case 1:
                            selection = inq_select("Which ally do you want to inspect?", *party)
                            selection = party[selection-1]
                            get_char_stats(selection)

                        case 2:
                            if benched_allies:
                                open_spot = inq_select("Which ally do you want to bench?", party[1], party[2])
                                ally_to_replace = party[open_spot]

                                new_party_member = benched_allies[inq_select("Which ally do you want to add to the team?", *benched_allies) - 1]

                                party[open_spot] = new_party_member
                                benched_allies.remove(new_party_member)
                                benched_allies.append(ally_to_replace)
                            else:
                                input("There are no spare allies!")
                        
                        case 3:
                            continue
                case 3:
                    for item in player_data['inventory']:
                        print(item)

                    input("Enter anything once you're done reading.")
                case 4:
                    save_dlc()
                case 5:

                    player_data['inventory'] = []
                    party = [player]

                    input("Exiting to main menu...")
                    return 0
        else:
            match inq_select(f"What do you want to do in {location['name']}?", "Explore", "Inspect Team", 'Inventory', "Proceed To Next Location", "Save", "Exit To Main Menu"):
                case 1:
                    dlc_explore(location)
                case 2:
                    match inq_select(f"Stats: \nDurability: {player_data['durability']} \nBravery: {player_data['bravery']} \nStrength: {player_data['strength']} \nRecovery: {player_data['recovery']} \nWhat do you want to do?", "Inspect Party Members", "Change Party Composition", "Back"):
                        case 1:
                            selection = inq_select("Which ally do you want to inspect?", *party)
                            selection = party[selection-1]
                            get_char_stats(selection)

                        case 2:
                            if benched_allies:
                                open_spot = inq_select("Which ally do you want to bench?", party[1], party[2])
                                ally_to_replace = party[open_spot]

                                new_party_member = benched_allies[inq_select("Which ally do you want to add to the team?", *benched_allies) - 1]

                                party[open_spot] = new_party_member
                                benched_allies.remove(new_party_member)
                                benched_allies.append(ally_to_replace)
                            else:
                                input("There are no spare allies!")
                        
                        case 3:
                            continue
                case 3:
                    for item in player_data['inventory']:
                        print(item)

                    input("Enter anything once you're done reading.")
                case 4:
                    break
                case 5:
                    save_dlc()
                case 6:

                    player_data['inventory'] = []
                    party = [player]

                    input("Exiting to main menu...")
                    return 0

    menu(dlc_locations[index + 1], index + 1)
