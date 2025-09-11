from game_assets import *
import random

ent_ai_enemies = []
ent_ai_allies = []

def enemy_decision_tree(enemy):
    # Extract attack types using getatt
    attack_list = getattr(enemy, "attacks", [])
    status_ability_list = getattr(enemy, "abilities", [])
    healing_ability_list = getattr(enemy, "heals", [])

    enemy_team = ent_ai_enemies
    player_team = ent_ai_allies

    decision_list = ["attack", "ability", "heal"]

    low_hp_enemies = []
    near_death_enemies = []
    damaged_allies = []
    critical_allies = []

    # Evaluate enemy team (AI's allies)
    for enemy_unit in enemy_team:
        hp_percent = (enemy_unit.hp * 100) / enemy_unit.max_hp
        if hp_percent <= 40:
            low_hp_enemies.append(enemy_unit)
        if hp_percent <= 20:
            near_death_enemies.append(enemy_unit)

    # Evaluate player team (AI's enemies)
    for ally in player_team:
        hp_percent = (ally.hp * 100) / ally.max_hp
        if hp_percent <= 60:
            damaged_allies.append(ally)
        if hp_percent <= 20:
            critical_allies.append(ally)
                                                                                                                   
    # Include self in healing logic
    self_hp_percent = (enemy.hp * 100) / enemy.max_hp
    if self_hp_percent <= 60:
        damaged_allies.append(enemy)
    if self_hp_percent <= 20:
        critical_allies.append(enemy)

    # HEAL weighting logic
    if healing_ability_list:
        if near_death_enemies:
            decision_list.extend(["heal"] * 3)
        if damaged_allies:
            decision_list.extend(["heal"] * 2)

    # ATTACK weighting logic
    if attack_list:
        if critical_allies:
            decision_list.extend(["attack"] * 3)
        elif damaged_allies:
            decision_list.extend(["attack"] * 2)

    # ABILITY weighting logic
    if status_ability_list:
        if low_hp_enemies:
            decision_list.extend(["ability"] * 2)
        if damaged_allies:
            decision_list.append("ability")

    # Randomly choose a valid action based on weighted list
    while True:
        main_choice = random.choice(decision_list)

        if main_choice == "attack" and attack_list:
            return random.choice(attack_list)
        if main_choice == "ability" and status_ability_list:
            return random.choice(status_ability_list)
        if main_choice == "heal" and healing_ability_list:
            return random.choice(healing_ability_list)


 
# --- Example Attacks and Abilities using game_assets.attack ---

from game_assets import attack

slash = attack("slash", "Slash", "A quick slash with a blade.", 15, 0, True, False,
               "slashes fiercely!", "slashes!", "misses the slash!", "completely whiffs!", None)

fireball = attack("fireball", "Fireball", "Launches a fireball that hits all enemies.", 10, 5, True, True,
                  "engulfs the enemies in flames!", "hits with a fireball!", "fireball fizzles.", "burns their own hand!", None)

single_heal = attack("single_heal", "Single Heal", "Heals one ally significantly.", -30, 4, False, False,
                     "heals deeply!", "restores health!", "healing falters.", "drops the herbs!", None)

group_heal = attack("group_heal", "Group Heal", "Heals all allies a small amount.", -10, 6, False, True,
                    "waves healing light!", "casts group heal!", "misfires the spell.", "heals the enemy!", None)

pocket_sand = attack("pocket_sand", "Pocket sand", "Deals damage and blinds the enemy.", 10, 3, True, False,
                      "hits eyes directly!", "blinds the foe!", "only a tiny goes in their eye!", "you somehow throw it 90° to the left, and miss completly!", 1)

shield_up = attack("shield_up", "Shield Up", "Raises a shield to reduce incoming damage.", 0, 2, False, False,
                   "perfect defense!", "raises a shield.", "shield slips!", "drops the shield!", 2)

# Function call
#print(test_enemy_decision_tree(player))





