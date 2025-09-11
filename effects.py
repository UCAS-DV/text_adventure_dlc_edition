from game_assets import *
turn = 0


timers = {}

effects_ids = {
    1: "blindness",
    2: "sheilded",
    3: "terrified"
}

def apply(effect_ids, char):
    if isinstance(effect_ids, int):
        effect_ids = [effect_ids]  # Wrap single int into a list

    if not effect_ids:
        return

    for effect_id in effect_ids:
        if effect_id is not None and effect_id not in char.effects:
            char.effects.append(effect_id)
            timers[(char.name, effect_id)] = turn
            # print(f"{char.name} is now affected by effect {effect_id}")


def track(characters):
    to_remove = []

    for char in characters:
        for effect_id in char.effects:
            key = (char.name, effect_id)

            # Effect logic
            run_effect_logic(effect_id, char)

            if key in timers and turn - timers[key] >= 3:
                to_remove.append((char, effect_id))

    for char, effect_id in to_remove:
        char.effects.remove(effect_id)
        del timers[(char.name, effect_id)]
        input(f"{char.name}'s effect {effects_ids[effect_id]} has worn off")

def run_effect_logic(effect_id, target):
    if effect_id == 3:  # terrified
        target.nerves = max(target.min_nerves, target.nerves - 5)
        print(f"{target.name} loses 5 nerves from terrified")