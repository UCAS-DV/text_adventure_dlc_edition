from game_assets import *
from save_load import player_data
from math import ceil

def level_up(allies, stat, degree):

    match stat:
        # Durability
        case 1:
            
            for ally in allies:
                ally.max_hp += ceil(20 * degree)
                ally.hp += ceil(20 * degree)

            player_data['durability'] += 1
            input(f"You're durability is at level {player_data['durability']}")
        # Bravery
        case 2:
            for ally in allies:
                ally.max_nerves += ceil(25 * degree)
                ally.nerves += ceil(25 * degree)
                ally.min_nerves += 10

            player_data['bravery'] += 1
        # Strength
        case 3:
            for ally in allies:
                for attack_ in ally.attacks:
                    attack_.hp *= 1.25 * degree
                    attack_.nerves *= 1.25 *degree

                    attack_.hp = ceil(attack_.hp)
                    attack_.nerves = ceil(attack_.nerves)

            player_data['strength'] += 1
        # Recovery
        case 4:
            for ally in allies:
                for heal in ally.heals:
                    heal.hp *= 1.35 * degree
                    heal.nerves *= 1.35 * degree

                    heal.hp = ceil(heal.hp)
                    heal.nerves = ceil(heal.nerves)

            player_data['recovery'] += 1
