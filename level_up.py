from game_assets import *
from save_load import player_data
from math import ceil

def level_up(allies, stat):

    match stat:
        # Durability
        case 1:
            for ally in allies:
                ally.max_hp += 10
                ally.hp += 10

            player_data['durability'] += 1
        # Bravery
        case 2:
            for ally in allies:
                ally.max_nerves += 25
                ally.nerves += 25
                ally.min_nerves += 25

            player_data['bravery'] += 1
        # Strength
        case 3:
            for ally in allies:
                for attack_ in ally.attacks:
                    attack_.hp *= 1.25
                    attack_.nerves *= 1.25

                    attack_.hp = ceil(attack_.hp)
                    attack_.nerves = ceil(attack_.nerves)

            player_data['strength'] += 1
        # Recovery
        case 4:
            for ally in allies:
                for heal in ally.heals:
                    heal.hp *= 1.35
                    heal.nerves *= 1.35

                    heal.hp = ceil(heal.hp)
                    heal.nerves = ceil(heal.nerves)

            player_data['recovery'] += 1
