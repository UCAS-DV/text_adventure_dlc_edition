# Attacks targe 
from dialogue_reader import *
from helper_funcs import inq_select
import game_assets
import random
import ent_ai
import os
import effects
from save_load import *

# Attacks target   
def attack_them(att, dealer, targets, nerves):

    if att.ability:
        for i in range(len(att.ability)):
            for j in range(len(targets)):
                effects.apply(att.ability[i],targets[j])

    # Rolls random multipler based off of nerves
    def roll_nerves(nerves, max_nerves ,attack, target):

        roll = random.randint(1,max_nerves)
        if attack != game_assets.pep_talk:
            if roll < nerves * 0.1:
                read_description(attack.super_success + [f'{attack.name} was super successful!'], target)
                return 1.5
            elif roll <= nerves:
                read_description(attack.success + [f'{attack.name} was successful!'], target)
                return 1
            if roll > nerves * 1.5:
                read_description(attack.super_fail + [f'{attack.name} was a complete failure!'], target)
                return 0.0001
            elif roll > nerves:
                read_description(attack.fail + [f'{attack.name} was ineffective!'], target)
                return 0.5
        else:
            read_description(attack.success + [f'{attack.name} was successful!'], target)
            return 1

    print("\033c")
    input(f'{dealer.name} uses {att.name}!')

    dmg = att.hp
    discomfort = att.nerves

    nerve_multiplier = roll_nerves(nerves, dealer.max_nerves, att, targets[0])

    # Multiply damage and nerve damage by nerve multiplier
    dmg = dmg * nerve_multiplier
    discomfort *= nerve_multiplier

    for target in targets:

        #print(target.effects)

        # Blindness deals 25% more damage
        if 1 in target.effects:
            
            if dmg > 0: 
                dmg *= 1.25
                dmg = round(dmg)
                print(f'{target.name} took {dmg - round(dmg/1.25)} more damage due to blindness')
            if discomfort > 0: 
                discomfort *= 1.25
                discomfort = round(discomfort)
                print(f'{target.name} lost {discomfort - round(discomfort/1.25)} more nerves due to blindness')

        # Shielded resists 25% of damage
        if 2 in target.effects:
            if dmg > 0: 
                dmg *= 0.75
                dmg = round(dmg)
                print(f'{target.name} resisted {round(dmg / 0.75) - dmg} points of damage due to being shielded')
            if discomfort > 0: 
                discomfort *= 0.75
                discomfort = round(discomfort)
                print(f'{target.name} resisted {round(discomfort / 0.75) - discomfort} points of nerve loss due to shielded')

        dmg = round(dmg)
        target.hp -= dmg

        discomfort = round(discomfort)
        target.nerves -= discomfort

        # Sets hp to 0 if it's below 0
        if target.hp < 0:
            target.hp = 0
        elif target.hp > target.max_hp:
            target.hp = target.max_hp

        # Sets nerves to minimum if it's below minimum
        if target.nerves < target.min_nerves:
            target.nerves = target.min_nerves
        elif target.nerves > target.max_nerves:
            target.nerves = target.max_nerves

        # Print the amount of damage done
        if dmg < 0:
            print(f'{dealer.name} gave {target.name} {-dmg} health!')
        elif dmg > 0:
            print(f'{dealer.name} dealt {dmg} damage to {target.name}!')

        # Print the amount of discomfort done
        if discomfort < 0:
            print(f'{dealer.name} gave {target.name} {-discomfort} nerves!')
        elif discomfort > 0:
            print(f'{dealer.name} removed {discomfort} nerves from {target.name}!')

        # Apply the effect
        #effects.apply(att.ability, target)

# Formats items so it can be used in UI
def format(unformatted_list):

    list_info = []
    for list_item in unformatted_list:
        list_info.append(f'{list_item}')

    list_info.append('Back')

    return list_info

# UI for choosing something from the list
def choose(prompt, selection_list):
    list_info = format(selection_list)

    try:
        selection = selection_list[inq_select(prompt, *list_info) - 1]
        return selection
    except:
        return 'Back'
    
# Selects random member from list
def select_random(selection_list):
    return selection_list[random.randint(0, len(selection_list) - 1)]

# Applies item effects
def use_item(item, allies, enemies):

    print("\033c")
    input(f'{game_assets.player.name} uses {item.name}!')

    while True:
        if item.offensive:
            # IF item affects multiple enemies
            if item.multi:

                target = game_assets.all_enemies

                read_description(item.a_desc, target)

                # Applies effects to all enemies
                for enemy in enemies:  
                    if enemy.hp > 0:
                        enemy.hp += item.hp
                        enemy.nerves += item.nerves

                input(f'All enemies lost {-item.hp} health.\nAll enemies lost {-item.nerves} nerves.')
                
                break
            else:
                
                # Print out all enemy info and have user select enemy
                enemy_info = format(enemies)

                enemy_selected = choose('Which enemy would you like to use your item on? ', enemies)

                if enemy_selected == 'Back':
                    break

                target=enemy_selected

                enemies.remove(enemy_selected)

                read_description(item.a_desc, target)

                # Apply Effects
                enemy_selected.hp += item.hp
                enemy_selected.nerves += item.nerves

                enemies.append(enemy_selected)

                target = enemy_selected

                input(f'{enemy_selected.name} lost {-item.hp} health.\n{enemy_selected.name} lost {-item.nerves} nerves.')
                
                break
        else:
            # IF item affects multiple allies
            if item.multi:
                
                # Applies effects to all allies
                for ally in allies:  
                    if ally.hp > 0:
                        ally.hp += item.hp
                        ally.nerves += item.nerves

                target = game_assets.all_allies

                read_description(item.a_desc, target)

                input(f'All allies gained {item.hp} health.\nAll enemies gained {item.nerves} nerves.')

                break
            else:
                
                # Print out all enemy info and have user select enemy
                ally_info = format(allies)
                ally_selected = choose('Which ally would you like to select? ', allies)

                if ally_selected == 'Back':
                    break

                target = ally_selected
                allies.remove(ally_selected)

                # Apply Effects
                ally_selected.hp += item.hp
                ally_selected.nerves += item.nerves

                allies.append(ally_selected)   

                read_description(item.a_desc, target)

                input(f'{ally_selected.name} gained {item.hp} health.\n{ally_selected.name} gained {item.nerves} nerves.')

                break
    return allies, enemies

# Main battle function
def battle(allies, enemies, opening, closing, inventory):
    #print(allies)
    #print(enemies)
    
    ent_ai.ent_ai_allies = allies
    ent_ai.ent_ai_enemies = enemies
    
    all = allies+enemies

    read_dialogue(opening)

    saved_inventory = inventory

    turn = 0
    effects.turn = turn
    battle_ended = False
    victory = False

    for combatant in all:
        combatant.effects = []

    while not battle_ended:

        
        # Checks if every ally has been knocked down
        lost = True
        for ally in allies:
            if ally.hp > 0:
                lost = False

        # Checks if every enemy has been knocked down
        won = True
        for enemy in enemies:
            if enemy.hp > 0:
                won = False

        if lost:

            # Resets enemy stats
            for enemy in enemies:
                enemy.hp = enemy.max_hp
                enemy.nerves = enemy.max_nerves

            # Resets allied stats
            for ally in allies:
                ally.hp = ally.max_hp
                ally.nerves = ally.max_nerves

            victory = False
            battle_ended = True
            break

        if won:
            
            # Resets allied stats
            for ally in allies:
                ally.hp = ally.max_hp
                ally.nerves = ally.max_nerves

            victory = True
            battle_ended = True
            break
        
        # IF player's turn
        if turn % 2 == 0:
            player_acted = False
            match inq_select('Which action would you like to perform?', 'Check Stats', 'Attack', 'Use Item', 'Run Away'):

                # Check Stats
                case 1:
                    match inq_select('Whose stats would you like to look at?', 'Team', 'Enemies', 'All'):
                        # Team Stats
                        case 1:
                            for ally in allies:
                                print(ally)
                        # Enemies Stats
                        case 2:
                            for enemy in enemies:
                                print(enemy)
                        # All Stats
                        case 3:
                            for ally in allies:
                                print(ally)
                            for enemy in enemies:
                                print(enemy)
                    continue

                # Attacks
                case 2:

                    ally_info = format(allies)
                    ally_selected = choose('Which ally would you like to select? ', allies)

                    if ally_selected == 'Back':
                        continue

                    # IF ally is not downed
                    if ally_selected.hp > 0:

                        all_actions = ally_selected.attacks + ally_selected.abilities + ally_selected.heals

                        attack_selected = choose('Which attack would you like to select? ', all_actions)
                        
                        if attack_selected == 'Back':
                            continue

                        target = None

                        # IF attack is not a multi attack, ask player to select one target
                        if not attack_selected.multi:
                            
                            # IF attack is offensive
                            if attack_selected.offensive:
                                target_info = format(enemies)
                                                             
                                try:
                                    target = enemies[inq_select('Which enemy would you like to attack? ', *target_info) - 1]
                                except:
                                    pass
                            else:

                                try:
                                    target = allies[inq_select('Which ally would you like to select? ', *ally_info) - 1]
                                except:
                                    pass
                            
                            # Only attack choosen target if target is not downed
                            try:
                                if target.hp > 0:
                                    attack_them(attack_selected, ally_selected, [target], ally_selected.nerves)
                                else:
                                    input('Oops! Seems like your target is already downed')
                            except:
                                pass

                        # IF attack is a multi attack
                        else:
                            
                            # Attack/Affect ALL targets depending if attack if offensive
                            if attack_selected.offensive:
                                attack_them(attack_selected, ally_selected, enemies, ally_selected.nerves)
                                player_acted = True
                                turn += 1
                                effects.turn = turn
                            else:
                                attack_them(attack_selected, ally_selected, allies, ally_selected.nerves)
                                player_acted = True
                                turn += 1
                                effects.turn = turn

                    else: 
                        input('Oops! Seems like you selected a downed ally!')
                        continue

                    if target != None:
                        if target.hp > 0:
                            player_acted = True
                            turn += 1
                            effects.turn = turn

                
                # Use Item
                case 3:

                    item_info = format(saved_inventory)

                    item_selected = choose('Which item would you like to select? ', saved_inventory)

                    if item_selected == 'Back':
                        continue
                    
                    allies, enemies = use_item(item_selected, allies, enemies)
                    saved_inventory.remove(item_selected)

                    turn += 1
                    effects.turn = turn

                case 4:

                    input('You ran away (Enter to Continue)')

                    # Resets enemy stats
                    for enemy in enemies:
                        enemy.hp = enemy.max_hp
                        enemy.nerves = enemy.max_nerves

                    # Resets allied stats
                    for ally in allies:
                        ally.hp = ally.max_hp
                        ally.nerves = ally.max_nerves

                    victory = False
                    battle_ended = True
                    break


            if player_acted:
                effects.track(all)
                input("-~-~-~-~- ENEMIES' TURN -~-~-~-~-")
                
        # Enemy Turn (Amber)
        else:

            while True:
                dealing_enemy = select_random(enemies)

                if dealing_enemy.hp > 0:
                    break
                    
                all_enemies_down = True

                for enemy in enemies:
                    if enemy.hp > 0:
                        all_enemies_down = False

                if all_enemies_down:
                    break

            attack = ent_ai.enemy_decision_tree(dealing_enemy)
            
            if attack.offensive:
                enemy_target = select_random(allies)

                if enemy_target.hp <= 0:
                    continue
            else:
                enemy_target = select_random(enemies)

                if enemy_target.hp == enemy_target.max_hp or enemy_target.hp <= 0:
                    continue

            if not attack.multi:
                input(f'{dealing_enemy.name} is taking the turn!')
                attack_them(attack, dealing_enemy, [enemy_target], dealing_enemy.nerves)
            else:
                if attack.offensive:
                    input(f'{dealing_enemy.name} is taking the turn!')
                    attack_them(attack, dealing_enemy, allies, dealing_enemy.nerves)
                else:
                    input(f'{dealing_enemy.name} is taking the turn!')
                    attack_them(attack, dealing_enemy, enemies, dealing_enemy.nerves)

            turn += 1
            effects.turn = turn

    if victory:
        input('===================== YOU WON ===================== \n(Enter to Continue)')
        read_dialogue(closing)
        return victory, saved_inventory
    else:
        input('===================== YOU LOSE ===================== \n(Enter to Continue)')
        return victory, inventory
    

#list1 = ["poop", "joe"]
#list2 = ["yourmother", "swanson"]
#list3 = list1+list2
#print(list3)
