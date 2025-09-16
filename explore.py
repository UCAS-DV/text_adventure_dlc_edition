from game_assets import *
from battle import battle
from save_load import player_data
from save_load import save_game
from save_load import load_game
from dialogue_reader import *
from helper_funcs import inq_select

# Avery, exploring

# Each main location now has unique mini-locations
main_locations = [
    {
        "name": "Spookyland",
        "mini_locations": ["Strength Tester", "Pumpkin Patch", "Ring Toss", "Haunted House", "Entrance"],
        'mini_local_desc': [[''],
                            ['You enter the 87th Annual Spookyland Pumpkin Patch of the carnival!',
                             'Given that this is Spookyland, all of the pumpkins are alive!',
                             '"Hey! Human!" says one of the pumpkins.',
                             '"I can make you rich and famous!"',
                             '"Just you wait! I will be the greatest pumpkin the world has ever seen!"',
                             '"I am going solve homelessness and poverty."',
                             '"I am gonna be the greatest philanthropist."',
                             'As you listen to the pumpkin, a skeleton with carving tools picks it up and takes it away.',
                             '"Just you wait!" says the pumpkin.', "I don't think we're gonna see it again..."],
                            ['You find a ring toss game without an operator.',
                             "There's a sign reading:", '"To the no one who is playing this game. Just take a prize. I really do not care."',
                             'You shrug and take a bagged goldfish.'],
                            [''],
                            ['']],
        "intro": 'Dialogue/spookyland_entrance.txt',
        "npc": {'dialogue': "Dialogue/carnival_skeleton.txt", 'position': 1},
        "item": {'item': spookyland_item, 'position': 3},
        "boss": {'boss_encounter': skellybones_fight, 'position': 5},
        "ally": skellybones_ally,
        "encounter": {'fight': spooky_monsters_fight, 'position': 4},
    },
    {
        "name": "Area 51",
        "mini_locations": ["Alien Lab", "Crash Site", "Hologram Hall", "Containment Cell", "Hover Pad"],
        "intro": "Dialogue/area_51/area_51_intro.txt",
        "mini_local_desc": [
            [
                ''
            ],
            [
                "You approach the crash site of what appears to be... a UFO made entirely of pretzel rods.",
                "Zeep is saluting the wreckage. \"Vrankle snackle norb!\" he sobs.",
                "A strange mist begins to rise, and your shoes begin to hum.",
                "This is probably fine."
            ],
            [
                "You enter the Hologram Hall, where fake presidents debate holographic goats.",
                "Zeep is at the podium arguing with a projected pinecone.",
                '"Dap no streeple vink!" he shouts. You nod solemnly.',
            ],
            [
                "You open a containment chamber.",
                "Inside is a small, glowing cat with antennae.",
                "It hisses and transmits NPR directly into your brain.",
                "Zeep Vorp appears. \"Blorp kitty zoom! Meeow-meeps!\"",
                "You nod and take the cat.",
                "It now owns you."
            ],
            [
                "The Hover Pad is quiet—too quiet.",
                "Zeep presses a button on a remote. A cow levitates into the air and vanishes.",
                '"Moo flarn doop!" he cheers. You are offered a seat on the next lift... you decline.'
            ]
        ],
        "npc": {
            "dialogue": "Dialogue/area_51/zeep_vorp.txt",
            "position": 1
        },
        "item": {
            "item": alien_cat,
            "position": 4,
            "dialogue": "Dialogue/area_51/alien_cat.txt"
        },
        "boss": None,
        "ally": zeep_vorp_ally,
        "encounter": {'position': None}
    },
    {
        "name": "North Pole",
        "mini_locations": ["Parade", "Sleigh Garage", "Elf Dorms", "Gift Storage", "Reindeer Lounge"],
        'mini_local_desc': [[''],
                            ['After ascending some flights of stairs,', 'you find the sleigh garage.',
                             'About a dozen sleighs in varying conditions are lined up to (very jolly) garage doors.',
                             'You accidentally press a button to open one of the doors.',
                             'The door is about 17 stories up, and leads to no where but the sky.',
                             'You continue to look around and you actually find a present in one of the sleighs labeled,',
                             '"Jackson Spook, Spookyland, 2017."', "Since it's dated about 8 years ago, you shrug and take it."],
                            [''],
                            [''],
                            ['You wander back down to the main floor and find a backdoor.',
                             'You open the door to find three reindeers playing a card game in a poorly lit room.',
                             'Two of them have artificial red noses but one of them has a genuine red nose,',
                             'Rudolph.',
                             'You take out a page of the constitution and a pen to try to get an autograph but get stopped by Mr. Skellybones.',
                             '"Raaaah, honored one, I trust your judgement but are you sure you would like to deface the constitution for a simple autograph."',
                             "He is right. You're about to deface the constitution, the most sacred document in all of the EMUSA, for an autograph.",
                             'Are you sure?', '...', 'You walk away with an autograph from Rudolph, the Red-Nosed Reindeer.']],
        'intro': 'Dialogue/north_pole/north_pole_intro.txt',
        "npc": {'dialogue': 'Dialogue/north_pole/mrs_claus.txt', 'position': 4},
        "item": {'item': present_item, 'position': 2},
        "boss": {'boss_encounter': santa_fight, 'position': 1},
        "ally": pepper,
        "encounter": {'fight': spec_ops_fight, 'position': 3},
    },
    {
        "name": "White House",
        "mini_locations": ["Oval Office", "War Room", "Garden"],
        'mini_local_desc': [[''],
                            ['You stumble into the War Room and notice a block of something on the table.',
                             'You take it out of curiosity.'],
                             ['']],
        'intro': 'Dialogue/white_house/white_house_intro.txt',
        "npc": {'dialogue': 'Dialogue/white_house/president.txt', 'position': 1},
        "item": {'item': patriotism, 'position': 2},
        "boss": {'boss_encounter': zeep_vorp_fight, 'position': 3},
        "ally": None,
        "encounter": {'position': None},
    }
]

# Adds items to inventory
def add_to_inventory(item):
   save_game({'location': load_game()['location'], 'allies': load_game()['allies'], 'inventory': load_game()['inventory'] + [item]})

# Starts encounter
def local_encounter(encounter):
   return battle(load_game()['allies'], encounter.enemies, encounter.opening, encounter.closing, load_game()['inventory'])

def explore(location, index):
    # Go through all main locations

    input(f"\n== Entering {location['name']} ==")

    read_dialogue(location['intro'])

    explored = []
    seen_npcs = set()
    victory = False
    boss_victory = False
    found_item = False
    left = False

    while not left:

        if index == 3:
            save_game({
            "location": 3,
            "allies": [player, skellybones_ally, zeep_vorp_ally, pepper],
            "inventory": load_game()['inventory']
            })

        if not boss_victory:
            choice = inq_select('Which place would you like to go?', *location['mini_locations'])

            selected = location["mini_locations"][int(choice) - 1]
        else:
            options = location['mini_locations'] + ['Exit']
            
            choice = inq_select('Which place would you like to go?', *options)

            try:
                selected = location["mini_locations"][int(choice) - 1]
            except:
                choice = inq_select('Are you sure?', 'No', 'Yes')

                if choice == 1:
                    continue
                else:
                    left = True
                    break

        # Read place description
        print(f"\nExploring {selected}...")

        # IF not at an npc, encounter, or boss fight, read place description
        if choice != location['npc']['position'] or choice != location['encounter']['position'] or choice != location['boss']['position']:
            read_description(location['mini_local_desc'][int(choice) - 1], all_allies)

        # IF at NPC location, read NPC dialogue
        if choice == location['npc']['position']:
            read_dialogue(location['npc']['dialogue'])
            if location['boss'] == None:
                boss_victory = True

        # IF at encounter location, enter encounter
        if location['encounter']['position'] != None:
            if choice == location['encounter']['position'] and victory == False:
                victory, player_data['inventory'] = local_encounter(location["encounter"]['fight'])
                
        explored.append(selected)

        # IF at item location, get item
        if choice == location["item"]['position'] and not found_item:
            print(f"\nYou have found the item: {location['item']['item'].name}!")
            add_to_inventory(location["item"]['item'])
            found_item = True

        # Now start the boss fight if there is one
        if location['boss'] != None:
            if choice == location["boss"]['position']:
                boss_victory, player_data['inventory'] = local_encounter(location["boss"]['boss_encounter'])

    if location['ally'] != None:
        if location["ally"] and location["ally"] not in player_data['allies']:
            print(f"{location['ally'].name} has joined your team!")
            player_data['allies'].append(location["ally"])

    player_data['location'] = index + 1
    player_data['inventory'] = load_game()['inventory']
    save_game(player_data)
        
# explore(main_locations[1], 1)