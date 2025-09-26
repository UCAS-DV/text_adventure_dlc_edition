debug_mode = False

class enemy:
    def __init__(self, name, enemy_class, max_hp, max_nerves, min_nerves, attacks, abilities, effects, heals):
        self.name = name
        self.enemy_class = enemy_class

        self.max_hp = max_hp
        self.hp = max_hp

        self.max_nerves = max_nerves
        self.nerves = max_nerves
        self.min_nerves = min_nerves

        self.attacks = attacks
        self.abilities = abilities
        self.effects = effects
        self.heals = heals

    def __str__(self):
        stats = f'-~-~-~-~-{self.name}-~-~-~-~-\nClass: {self.enemy_class} \nHP: {self.hp}/{self.max_hp}\nNerves: {self.nerves}/{self.max_nerves}\nMinimum Nerves: {self.min_nerves}\n'


        if 2 in self.effects:
            stats += f'    Shielded - 25% damage resistance'

        if 1 in self.effects:
            stats += f'    Blinded - 25% damage vulnerability'

        if 3 in self.effects:
            stats += f'    Terrified - Loses 5 nerves per turn'

        return stats

class ally:
    def __init__(self, name, max_hp, max_nerves, min_nerves, attacks, abilities, effects, heals):
        self.name = name

        self.max_hp = max_hp
        self.hp = max_hp

        self.max_nerves = max_nerves
        self.nerves = max_nerves
        self.min_nerves = min_nerves

        self.attacks = attacks
        self.abilities = abilities
        self.effects = effects
        self.heals = heals

    def __str__(self):
        stats = f'-~-~-~-~-{self.name}-~-~-~-~-\nHP: {self.hp}/{self.max_hp}\nNerves: {self.nerves}/{self.max_nerves}\nMinimum Nerves: {self.min_nerves}'


        if 2 in self.effects:
            stats += f'\n    Shielded - 25% damage resistance'

        if 1 in self.effects:
            stats += f'\n    Blinded - 25% damage vulnerability'

        if 3 in self.effects:
            stats += f'\n    Terrified - Loses 5 nerves per turn'

        return stats


class attack:
    def __init__(self, class_name, display_name, description, hp, nerves, offensive, multi, super_success, success, fail, super_fail, ability):
        #ADD ABILITY AFTER MULTI
        self.class_name = class_name
        self.name = display_name
        self.desc = description

        self.hp = hp
        self.nerves = nerves

        self.offensive = offensive
        self.multi = multi


        self.super_success = super_success
        self.success = success
        self.fail = fail
        self.super_fail = super_fail
        self.ability = ability

    def __str__(self):
        # Affects single enemy
        if self.offensive and not self.multi:
            string = f'{self.name}:\n    {self.desc}\n    Damage: {self.hp}\n    Nerves: {self.nerves}\n    Target: Enemy'
        # Affects multiple enemies
        elif self.offensive and self.multi:
            string = f'{self.name}:\n    {self.desc}\n    Damage: {self.hp}\n    Nerves: {self.nerves}\n    Target: All Enemies'
        # Affects single ally
        elif not self.offensive and not self.multi:
            string = f'{self.name}:\n    {self.desc}\n    HP Gained: {-self.hp}\n    Nerves: {-self.nerves}\n    Target: Ally'
        # Affects multiple allies
        elif not self.offensive and self.multi:
            string = f'{self.name}:\n    {self.desc}\n    HP Gained: {-self.hp}\n    Nerves: {-self.nerves}\n    Target: All Allies'

        if 2 in self.ability:
            string += f'\n    Applies Shielded which applies a 25% damage resistance.'

        if 3 in self.ability:
            string += f'\n    Applies Terrified which takes 5 nerves each turn.'

        return string

class item:
    def __init__(self, name, item_description, hp, nerves, offensive, multi, ability, action_description):
        self.name = name
        self.i_desc = item_description
        self.a_desc = action_description

        self.hp = hp
        self.nerves = nerves
        self.ability = ability
        
        self.offensive = offensive
        self.multi = multi

    def __str__(self):
        # Affects single enemy
        if self.offensive and not self.multi:
            return f'{self.name}:\n    {self.i_desc}\n    Damage: {-self.hp}\n    Nerves: {self.nerves}\n    Target: Enemy'
        # Affects multiple enemies
        elif self.offensive and self.multi:
            return f'{self.name}:\n    {self.i_desc}\n    Damage: {-self.hp}\n    Nerves: {self.nerves}\n    Target: All Enemies'
        # Affects single ally
        elif not self.offensive and not self.multi:
            return f'{self.name}:\n    {self.i_desc}\n    HP Gained: {self.hp}\n    Nerves: {self.nerves}\n    Target: Ally'
        # Affects multiple allies
        elif not self.offensive and self.multi:
            return f'{self.name}:\n    {self.i_desc}\n    HP Gained: {self.hp}\n    Nerves: {self.nerves}\n    Target: All Allies'

class encounter:
    def __init__(self, enemies, opening, closing):
        self.enemies = enemies
        self.opening = opening
        self.closing = closing

all_enemies = enemy('All enemies', 'All Enemies', 0, 0, 0, [], [], [], [])
all_allies = ally('All enemies', 0, 0, 0, [], [], [], [])

# ------------------------------------------------- Testing Assets Start ------------------------------------------------
test_enemy_attack = attack('sin_off', 'Test Attack 1', 'An attack for testing', 20, 20, True, False, ['0'], ['1'], ['2'], ['3'],[])
test_ally_attack = attack('sin_off', 'Test Attack 2', 'An attack for testing', 20, 20, True, False, ['0'], ['1'], ['2'], ['3'],[])
falcon_punch = attack('heal', 'FALCON PUNCH', 'An attack for testing', 2000, 2000, True, True, ['0'], ['1'], ['2'], ['3'],[])
resign = attack('heal', 'resign', 'An attack for testing', 2000, 2000, False, False, ['0'], ['1'], ['2'], ['3'],[])

sin_off_item = item(name='Item 1',item_description='An item made for testing!',hp=-20, nerves=-20,
                 action_description=['This is an item.', 'It is being used.'],
                 offensive=True, multi=False, ability=[])
mult_off_item = item(name='Item 2',item_description='An item made for testing!',hp=-20, nerves=-20,
                 action_description=['This is an item.', 'It is being used.'],
                 offensive=True, multi=True, ability=[])
sin_self_item = item(name='Item 3',item_description='An item made for testing!',hp=20, nerves=20,
                 action_description=['This is an item.', 'It is being used.'],
                 offensive=False, multi=False, ability=[])
mult_self_item = item(name='Item 4',item_description='An item made for testing!',hp=20, nerves=20,
                 action_description=['This is an item.', 'It is being used.'],
                 offensive=False, multi=True, ability=[])

test_inventory = [sin_off_item, mult_off_item, sin_self_item, mult_self_item]
test_attacks = [test_ally_attack, falcon_punch, resign]

test_enemy = enemy(name='Test Enemy', enemy_class='Tester',
                   max_hp=50, max_nerves=100, min_nerves=10,
                   attacks=[test_enemy_attack],abilities=[],effects=[],heals=[])

test_ally = ally(name='Test Ally', 
              max_hp=100, max_nerves=100, min_nerves=10, 
              attacks=[test_ally_attack],abilities=[],effects=[],heals=[])

# ================================================= Items =================================================
present_item = item(name='Present',item_description='Tragically, Jackson Spook never got his present in 2017. So sad.',hp=-5, nerves=-30,
                 action_description=['You pull out the present you got from earlier.', 'You open it to see a gaming console packed with a horror game.', 'You open it and hook it up to a nearby TV.',
                                     'The horror game is kinda mediocre but your gameplay is so horrendous that it stresses everyone out.', 'Seriously, I have never seen someone suck at a video game so much.',
                                     'Like, if life was a video game,', "you wouldn't have gotten past 3.", "Thank goodness that this is all real and life isn't a video game."],
                 offensive=True, multi=True, ability=[])


spookyland_item = item('Bagged Goldfish', "There's something off about this goldfish...", -30, -5, True, True, [],
                       ['For some reason you decide to use your goldfish you got from the carnival.', "You untie the bag, allowing the goldfish to see air.", 'The goldfish turns to your enemies and tells such a horrifying,',
                        'disturbing,', 'absolutely petrifying truth that no one can recover from.', 'The truth is so terrible that they actually suffer a heart attack for a brief moment as their heart stops from the shock.'])


patriotism = item('Block of Patriotism', 'A block of pure, unfiltered patriotism.', 50, 50, False, True, [], 
                  ['Harnessing the power of our forefathers,', 'of our great EMUSA,', 'you feel a sudden bout of patriotism flow through your veins.', '"Raaaaah, may the EMUSA last centuries longer!" says Mr. Skellybones',
                   '"Yeah! May the EMUSA shine brighter than the brightest stars!"', '"I have not felt this proud of anything before!"', '"Not even the glorious North Pole" says Pepper.', 'You nod proudly.', 'We have a country to save,', 'and nothing is stopping us.'])

alien_cat = item(
    name="Alien Cat",
    item_description="A purring space creature that hums at 432Hz and occasionally phases through walls.",
    hp=35,
    nerves=75,
    offensive=False,
    multi=False,
    ability=[],
    action_description=["The Alien Cat climbs onto your head and purrs", "You feel your neurons realign."]
    )

# ================================================= Bosses =================================================

# ------------------------------------------------- VIYH Moves -------------------------------------------------
pessimism = attack('pessimism', 'Terrible Pessimism', '', 0, 10, True, False,
                 ["To be frank, given how absolutely dysfunctional the country was,", "I don't even think it's worth it."],
                 ["I'm going to be honest, I don't think we, an unpaid intern and a voice in that intern's head can save America like Madam Vice President wants us to."],
                 ['I believe that you will make a mistake at some point in time!', 'Take that!'],
                 ["I have so many negative things to say but what's even the point of sharing them?", 'Does it even matter?'],[])
pep_talk_boss = attack('single_heal', 'Pep Talk', "Fear can't beat out the power of a good pep talk!", -10, -10, False, False, 
                      ['I give myself such an incredible, rousing self pep talk that even you feel a little inspired.', 'Wow, I should really pursue public speaking!', "You know, I think I might do so!", 'Yeah...', 'wait,', 'the only person who can hear me is you.', '...', 'Ow.'],
                     ['I give myself a pep talk and feel inspired by my own words.'], 
                     ["You know...", 'I am so happy that the only person who can hear me is you.'], 
                     ['Um...', "I thought I would be better at speaking given that it's the only thing I can do.", 'Just...', 'please forget everything I just said.'],[])
yell = attack('yell', 'Unbearable Yell', '', 10, 5, True, False,
              ['NO, YOU DID NOT WIN THAT ONLINE ARGUMENT LAST NIGHT!', 'YOU WERE JUST FLAT OUT WRONG!'],
              ["THE ORIGINAL MOVIE WASN'T THAT GOOD!", "YOU ARE JUST LOOKING AT IT WITH ROSE-TINTED GLASSES!"],
              ['aaaaaaa?'],
              ['Um...', 'uh...', "I don't have anywhere near enough energy to yell."], [])

viyh = enemy(name='The Voice In Your Head', enemy_class='All-Rounder',
             max_hp=50, max_nerves=100, min_nerves=10, 
             attacks=[pessimism, yell], abilities=[], effects=[], heals=[pep_talk_boss])

# ------------------------------------------------- Skellybones (Boss) -------------------------------------------------
bone_blow_boss = attack('bone_blow', 'Funny Bone Blow', '', 20, 0, True, False,
                   ["With what you think is a deadpan expression", "(you can't really tell because he's just a faceless skeleton)", 
                    "He lightly taps your funny bone.", "You look at him confused but suddenly... what feels like a jolt of lightening traverses through your arm and-",
                    '...', '...', 'You good?', 'It seems like your brain was too focused on writhing in very unfunny pain to remember to conjure my existence.', "Uh, don't do that again.",
                    "It's kind of a buzzkill."],
                    ['He hits your funny bone in a very unfunny way'],
                    ['He tries to hit your funny bone in a very unfunny way but he only lightly taps it'],
                    ['He tries to hit your funny bone but he trips and hits his own funny bone.', 'He lays on the ground immobilized as you look down at him with pity.',
                    '"THIS IS NOT FUNNY RAAAAAAH"', 'Eventually he gets his footing and the battle continues.'], [])
truth_enemy = attack('truth', 'Disturbing Truth', '', 0, 10, True, False,
                     ['He walks up to you and whispers to you...', '"Raaaah."', '[My lawyer has advised me to remove the following dialogue]'],
                     ['"Raaaah. 2017 was 8 years ago."', 'You feel disturbed.'],
                     ['"Raaaah. Some people are poor."', 'You feel a little bummed out.'],
                     ['Mr. Skellybones tries to disturb you but it ended up being such a blatant truth that you feel nothing.', 'You look at him with a deadpan expression.', 
                     'He feels a little embarressed.'], [3])
got_milk_enemy = attack('single_heal', 'Got Milk?', 'Milk makes your bones stronger!', -20, 0, False, False,
                        ['He reaches behinda grave and grabs a jug of Clarkplace(TM) milk.', '"Raaaah. Only Clarkplace Milk(TM) makes feel this good."', 
                        '"You can find Clarkplace Milk(TM) at your local PriceCo(TM) for only $4.29"', 'He tilts his skull in what you think is a wink and drinks the whole cartoon.', 
                        'He looks significantly more health y.'],
                        ['He reaches behind a grave and grabs a jug of Awesome Price(TM) milk.', 'He drinks it and looks revitalized.'],
                        ['He reaches behind a grave and grabs a jug of expired Awesome Price(TM) milk.', "He drinks it and seems disgusted," "you can't really tell because he's just a skeleton."],
                        ['He reaches behind a grave and grabs an empty jug of Clarkplace(TM) milk.', 'He looks at the jug with despair.', '"Raaaah. Why did you have to leave me too dear Clarkplace(TM) Milk"',
                        'You reconcile him as he despairs', '"Raaaah. Thank you"', "Now that he's feeling better, you hug and then continue the fight"], [])


skellybones_boss = enemy('Mr. Skellybones', 'Nerve Damager', 100, 100, 10,
                    [bone_blow_boss, truth_enemy], [], [], [got_milk_enemy])

skellybones_fight = encounter([skellybones_boss], 'Dialogue/skellybones_intro.txt', 'Dialogue/skellybones_outro.txt')

# ------------------------------------------------- Santa Claus Fight -------------------------------------------------
blast = attack('blast', 'Christmas MegaBlast', '', 20, 0, True, True, 
               ['"Hohoho!"', '"I did not want to go this far but I will if I must."', '"I CALL UPON EVERY GREAT POWERS BEFORE I,"',
                '"FROM FATHER CHRISTMAS TO KRIS KRINGLE,"', '"I HARNESS THEE FOR A..."', '"CHRISTMAS"', '"ULTRA"', '"BLAST!"', "For a moment, all you can see is red, green, and white.",
                'Once the blast is over, you notice a several meter wide whole blasted through the wall behind you with a trail spanning to the horizon.', 'How did you even survive that?',
                'Do you have plot armor or something?'],
                ['Santa harnesses his Christmas Spirit and does his iconic and famous Christmas MegaBlast,', 
                'Completely blinding you in its brilliance.', 'Oh, classic Santa!'],
                ['Santa attempts to harness his Christmas Spirit but it seems that the stress of preparing for Christmas has gotten to him.', 'His spirit is considerably weaker.'],
                ['"Hohoho!"', '"I wanted to go this far as much as you but you leave me no choice"', '"CHRISTMAS"', '"SUPER"', '"BLA-"', 'His hat falls off his head, cancelling his attack',
                '"Oh! Pardon me!"'], [])
intimidation = attack('intimidation', 'Intimidation', '', 0, 15, True, True,
                      ['Santa walks up to you and places a hand on your shoulder.', '"220 N 330 W, Amber Avenue."', 'He walks up to Zeep Vorp next', '"114.234.123.65"', 'Finally he approaches Mr. Skellybones.', '"(555) 245-5555"', '"Am I correct?"'],
                      ['Santa pulls out his naughty list and he writes a few names in it.', 'You and your team stress out, worried that he put your names on the list.'],
                      ["Santa begins to charge up a Christmas MegaBlast and you panic for a little bit, until you realize he's been charging it for longer than usual.", 
                        'So you shrug, walk up, and knock his hat off his head.'],
                      ['"Why you have tested my patience for too long."', '"I am going to say a horrible thing."', '"You will not even believe what I am about to say."',
                       'You stress out, worried that Santa is going to destroy his precious, pure image. You brace for the worst.', '"YOU ARE SUBPAR IN SOME OF YOUR HOBBIES!"', 
                       '"do not worry though, practice makes perfect"', '"BUT YOU WILL HAVE TO PRACTICE A LOT!"', 'Santa smirks, proud of his own audacity.'], [])
beam_enemy = attack('beam', 'Peppermint Beam', '', 30, 0, True, False,
              ['The elf stands back and gets ready for something.', 'She closes her eyes and starts yelling for some reason?.', 'Suddenly, she starts glowing the hat on her head turns from a dark green to a bright white.'
               '"SUPER"', '"PEPPER-"', '"MINT"', '"BEEEEEEEEEEEEAAAAAAAAAAAAAAMMMMMMMMMMM!"', 'The light from the beam is blinding.', "It's thin as paper but the damage is incredible."],
              ['The elf makes a finger gun and points it at {tname}.','"PEPPERMINT"', '"BEAM!', "The laser blasts out of her hand and burns with the heat of a thousand suns.", "It's extremely precise and Worst of all,", 'it tastes like peppermint.', 'Gross...'],
              ['"PEPPERMINT"', '""BLAST!"', 'Nothing happens.', '"Wait..."', '"That is not right."', '"Peppermint beam?"', "The beam fires out of her hands at {tname}, but because of the embarrasment of her initial blast, it's less powerful."],
              ['PEPPERMINT', 'BEAM!', 'At the speed of light, it fires out of her hand.', 'She smirks arrogantly, proud of her actions.', 'She completely missed.', 'Haha,', 'loser.'], [])
present_pepper = attack('present', 'Present', '', 0, 20, True, False,
                       ['Using her elf skills,', 'the elf quickly builds a teddy bear?', 'Huh, everyone looks at it adoringly.', 'But then, {tname} looks in its cold,', 'dead,', 'apathetic', 'eyes,', 'and is very disturbed by it.'],
                       ['Using her elf skills,', 'the elf quickly builds a water gun and fires it at {tname}.', "Now they're cold, wet, and not very happy."],
                       ['Using her elf skills,', 'the elf quickly builds one of those really mesmerizing fans that light up.', 'You know the one.', 'Anyway she turns it on and it mesmerizes {tname}.', '{tname} eventually regains control and is only a little panicked to see how much happened while he was in a trance.'],
                       ['Using her elf skills,', 'the elf quickly builds a sticky hand and flings it at {tname}.'], [])

santa = enemy('Santa Claus', 'AOE Damager', 100, 120, 10, [blast, intimidation], [], [], [])
agent_elf = enemy('Special Agent Elf', 'Focused Damager', 80, 120, 10, [beam_enemy, present_pepper], [], [], [])

santa_fight = encounter([santa, agent_elf], 'Dialogue/north_pole/santa_intro.txt', 'Dialogue/north_pole/santa_outro.txt')

# ------------------------------------------------- Zeep Vorp (Boss) -------------------------------------------------
super_charge = attack('charge', 'Super Proton Charge', 'Harness the power of the electromagnatism with a proton charge!', 25, 0, True, True,
                     ['It seems like Zeep Vorp remembered to set his proton charges to "Illegal everywhere except Texas" instead of "Mild Inconvience."'],
                     ['Zeep Vorp fires several super-proton charges at you and your team.'],
                     ['Zeep Vorp fires several super-proton charges but you and your team narrowly dodge out of the way.'],
                     ['Zeep Vorp tries to fire a bunch of super-proton charges at you but his mech jams.'], [])
replication = attack('replication', 'Replication', '', -20, -10, False, False,
                     ['Zeep somehow created a better, more evolved version of himself who kicked him out of the mech, fixed the mech, and took charge himself.'],
                     ['In what I can only describe as a crime against biology,', 'Zeep duplicates himself several times to tend to him and fix his ship as he pilots it.'],
                     ["Zeep duplicates himself several times to tend to him and fix his ship, but apparently it's hard to repair a flying mech's external wounds, as it is flying,",
                     'So nothing really gets done.', "They were able to stick a princess-branded bandages on it so I'm sure it's fine."],
                     ['In what I can only describe as an attempted crime against biology,', 'Zeep duplicates himself several times to tend to his own wounds and fix his ship as he pilots it...',
                     'but he forgot to duplicate his conscious so the clones just run off on their own endeavors.', "I hope they're okay, wherever they went."], [])
hologram = attack('hologram', 'Hologram', '', 0, 20, True, False,
                  ["Zeep Vorp activates a hologram showing {tname}'s greatest fear.", 'Even Mr. Skellybones is shocked at how scary Zeep Vorp can be.'],
                  ['Zeep Vorp activates several holograms of himself to confuse {tname}.'],
                  ['Zeep Vorp tries to activate several holograms of himself to confuse {tname}, but he trips and can only activate one because he broke the other 43.'],
                  ['Zeep Vorp tries to activate several holograms of himself to confuse {tname}, but it seems like he ran out of his free trial.', 'He spends a couple minutes trying to pay for Hologram+ and eventually he figures it out.', 'Sigh...', 'classic Zeep Vorp.'], [])

zeep_vorp_enemy = enemy('Zeep Vorp', 'All-Rounder', 120, 130, 30, [super_charge], [hologram], [], [replication])

zeep_vorp_fight = encounter([zeep_vorp_enemy], 'Dialogue/white_house/zeep_vorp_intro.txt', "Dialogue/white_house/zeep_vorp_outro.txt")

# ================================================= Encounters =================================================

# ------------------------------------------------- Very Spooky Monsters -------------------------------------------------
moral_support = attack('moral_support', 'Moral Support', '', -20, -10, False, False,
                       ['The ghost flies to the {tname}.', "The ghost reaches into itself and pulls out a bag of G&Gs and hands it to the {tname}.", '"I hope you know that you deserve this after all of your hard work!"', '{tname} smiles gently and eats the G&Gs.', "They taste absolutely horrendous but it's the thought that counts!"],
                       ['"Hooray for {tname}!" says the ghost', '"We all love {tname}! Heehee!"', 'The {tname} feels revitalized and motivated.'],
                       ['"Hooray for {tname}?" says the ghost', '"And um..."', '"Well...', '"A for effort?"'],
                       ['"OH COME ON!" says the ghost', '"THEY WERE RIGHT THERE!"', '"YOU-"', '"YOU-"', '"IMBECILES!"', 'Everyone looks at the ghost shocked.', 'You shake your head in disapproval', '"Oh..."', '"Uh..."', '"Hee hee?"'], [])

scare = attack('scare', 'Scare', '', 0, 10, True, False,
               ["You blink and the zombie's gone!", "Well that's awfully convienent.", "I'm sure nothing could go wrong!", 'You turn around to see the zombie right next to you.', 'It whispers in your ear, ', '"Your body replaces your cells every 7 to 10 years."',
                'AAAAAAAAAAAAA!', 'PHILOSOPHICAL DILLEMA!'],
                ['"Boo!"', 'Eek!'],
                ['"Boo?"', 'Eek?'],
                ["You blink and the zombie's gone!", "Well that's awfully convienent.", "Although I'm sure it's going to pop up and scare us.", "So be prepared!", '...', '...', '...', "It's been 15 minutes, what's the deal?",
                 "You see the zombie walk back.", '"Sorry, I went to go make sure I left my door locked before leaving."', '"I did!"', 'You shrug and continue the battle.'], [])

trick = attack('nudge', 'Trick', '', 15, 0, True, False,
               ['The zombie charges at you and you promptly run away.', 'You keep running until you realize that something is off.', 'You look down to find that you have just ran off a cliff.', 'You raise up a sign saying "Help" and fall all of the way down.',
                'Eventually you make it back up to the carnival.'],
               ['"Brains... trick or treat!"', 'You notice a shadow forming under you.', 'You look up to see a piano falling from the sky.', "It seems like we've been tricked...", 'The piano falls and crushes you.'],
               ['"Brains... trick or treat!"', ''],
               ['"Brains... trick or treat!"', 'You shake your head in disapproval, rejecting the zombie.', 'The zombie walks away defeated.', '"Rejected me just like Jessica..." the zombie says under its breath.'], [])

ghost = enemy('Very Spooky Ghost', 'General Healer', 55, 100, 30, [], [], [], [moral_support])
zombie_one = enemy('David', 'General Damager', 50, 100, 10, [trick, scare], [], [], [])
zombie_two = enemy('Very Spooky Zombie', 'General Damager', 40, 100, 10, [trick, scare], [], [], [])

spooky_monsters_fight = encounter([zombie_one, ghost], 'Dialogue/encounter_intro.txt', 'Dialogue/encounter_outro.txt')

# ------------------------------------------------- Spec. Ops. Elves -------------------------------------------------
present_enemy = attack('present', 'Present', '', 0, 20, True, False,
                       ['Using their elf skills,', 'the elf quickly sews some Christmas socks and gives it to {tname}.', 'The crippling disappointment meant devastates them.'],
                       ['Using their elf skills,', "the elf quickly builds spring toy that's slightly bent to {tname}.", 'The disappointment stings.'],
                       ['Using their elf skills,', "the elf quicklu sews a nice jacket.", 'They make it a slightly off color so it looks ugly.', 'They give it to {tname}.', "It looks a little off but hey, it's the thought that counts.", 'Although the thought was actively malicious...'],
                       ['Using their elf skills,', 'the elf quickly makes some chocolate.', 'They make it dark choclate expecting {tname} to dislike it,', 'but since {tname} is a good person,', 'they enjoy it!',], [])
shine = attack('shine', 'Shine', '', 10, 0, True, True,
               ["Using their cybernetic implant they got after Rudolph's fabled night,", 'the reindeer shines their nose at max brightness, completely blinding everyone.'],
               ["Using their cybernetic implant they got after Rudolph's fabled night,", 'the reindeer shines their nose, partially blinding everyone.'],
               ["Using their cybernetic implant they got after Rudolph's fabled night,", 'the reindeer shines their nose, but the battery is dying.', "It shines brightly for just a split second but it doesn't do a lot of damage."],
               ["Using their cybernetic implant they got after Rudolph's fabled night,", 'the reindeer shines their nose, but it seems like the battery is dead.', 'It finds a pair of AA batteries just to find out that the implant needs AAA batterires.', 'It searches around the factory and eventually finds the batteries it needs.'],
               [1])
snowball = attack('snowball', 'Snow Ball', '', 25, 10, True, False,
                  ['The elf makes a perfectly spherical snowball using magically summoned snow.', 'It tosses it with perfect precision.'],
                  ['The elf makes a decently spherical snowball using magically summoned snow.', 'It tosses it with masterful precision.'],
                  ['The elf makes a kind of spherical snowball using magically summoned snow', 'It tosses it but it barely hits you.'],
                  ['Like a complete IDIOT,', 'the elf makes a poorly formed snowball and COMPLETELY misses like a LOSER!'], [])

elf_one = enemy('Spec. Ops. Elf 1', 'Focused Damager', 50, 100, 30, [present_enemy, snowball], [], [], [])
elf_two = enemy('Spec. Ops. Elf 2', 'Focused Damager', 50, 100, 30, [present_enemy, snowball], [], [], [])
reindeer = enemy('Spec. Ops. Reindeer', 'AOE Effect Support', 70, 100, 20, [], [shine], [], [])

spec_ops_fight = encounter([elf_one, elf_two, reindeer], 'Dialogue/north_pole/spec_ops_intro.txt', 'Dialogue/north_pole/spec_ops_outro.txt')

# ================================================= Allies =================================================

# ------------------------------------------------- Player Moves -------------------------------------------------
kickflip = attack('sin_off', 'Kickflip', 'Wow everyone with a radical kickflip!', 20, 0, True, False, 
                  ['You run up and do the most rad', 'tubular', 'fresh', 'kickflip on {tname} the world has ever seen.'], 
                  ['You run up and RADICALLY kickflip {tname}.'], 
                  ['You run up and kickflip {tname} but it was only kinda cool.', 'Honestly, it was a 6/10 at best.'],
                  ['You run up and try to kickflip {tname} but you trip and fall onto a nearby skateboard.', 'You end up kickfliping the skateboard,', 'followed by 7 1080 flips', 
                   'and then a 1080 backflip off of the skateboard and onto another skateboard.', 'You end up winning the local "cool guy" competition but you dealt almost no damage.'],[])
declaration = attack('sin_off', 'Uncouth Declaration', "Forget physical damage! Emotional damage is where it's at!", 0, 15, True, False, 
                     ["Oh...", "wow...", "I get how intense this situation is but you didn't have to go that far.", "To be frank I don't even know if you can legally say that."],
                     ['You yell some very inflamatory statements.', 'The shock of your statements makes {tname} uneasy'], 
                     ['You yell some somewhat mean statements.', 'Honestly, {tname} is shocked at how you could come up with such mild statements'], 
                     ["Okay, so, pro tip...", 'Calling {tname} "Stinky" is not very effective past the first grade'],[])
pep_talk = attack('single_heal', 'Pep Talk', "Fear can't beat out the power of a good pep talk! (This works regardless of your nerves)", 0, -15, False, False, 
                     ['You give such an incredible, rousing self pep talk that even your enemies feel a little inspired.'],
                     ['You give an inspirational pep talk that relieves the stress of battle.'], 
                     ['You try to give yourself a pep talk but you suck at public speaking so it proves ineffective.'], 
                     ['...', "That was...", 'something.', "Don't beat yourself up about it,", 'just ensure that you will never have to do any sort of public speaking...', 'ever...'
        "and you'll be fine!"],[])
apple = attack('single_heal', 'Apple', 'As they say, an apple a day keep the doctor away! Although it might be better to have a doctor in this situation...', -20, 0, False, False,
                 ['The apple tastes funny.', 'In the bitemark you can see the signature of John Apple,', 'the inventor of apples.', "It's rumored that signed apples are only healthy if they deem the eater worthy.", 'Fortunately, the eater was worthy!'],
                 ["{tname} eats the apple and is as healthy as ever!"],
                 ['It seems that you have Gala apple.', "I guess it's healthy but did you seriously have to have the worst type of apple.", '{tname} eats the apple unhappily.', "Fortunately it's still healthy"],
                 ['The apple tastes funny.', 'In the bitemark you can see the signature of John Apple,', 'the inventor of apples', '"You are NOT worthy!"', 'says the apple as it dissappears.', 'It seems like {tname} was not worthy of a signed apple.'],[])


def load_player():

    if debug_mode:
        player_attacks = [kickflip, declaration, falcon_punch, resign]
    else:
        player_attacks = [kickflip, declaration]

    player = ally(name='Unpaid Intern', 
              max_hp=100, max_nerves=100, min_nerves=25, 
              attacks=player_attacks,abilities=[], effects=[],heals=[pep_talk, apple])
    
    return player

player = load_player()

# ------------------------------------------------- Skellybones (Ally) -------------------------------------------------
bone_blow_ally = attack('bone_blow', 'Funny Bone Blow', '"HEY! This is no laughing matter!', 10, 10, True, False,
                   ["With what you think is a deadpan expression", "(you can't really tell because he's just a faceless skeleton)", 
                    "He lightly taps {tname}'s funny bone.", "You look at him confused but suddenly {tname} shuts down completely.", "It's like someone turned {tname} off and on again"],
                    ["He hits {tname}'s funny bone in a very unfunny way."],
                    ["He tries to hit {tname}'s funny bone in a very unfunny way but he only lightly taps it"],
                    ["He tries to hit {tname}'s funny bone but he trips and hits his own funny bone.", 'He lays on the ground immobilized as you look down at him with pity.',
                    '"THIS IS NOT FUNNY RAAAAAAH"', 'Eventually he gets his footing and the battle continues.'], [])
truth_ally = attack('truth', 'Disturbing Truth', "Freak your opponents out with something mildly shocking!", 0, 5, True, True,
                     ['Mr. Skellybones stands and declares...', '"Raaaah."', '[My lawyer has advised me to remove the following dialogue]', 'You and your enemies are very disturbed'],
                     ['"Raaaah. 2017 was 8 years ago."', 'Everyone feels disturbed.'],
                     ['"Raaaah. Some people are poor."', 'Your enemies feels a little bummed out.'],
                     ['Mr. Skellybones tries to disturb your enemies but it ended up being such a blatant truth that they feel nothing.', 'Everyone looks at him with a deadpan expression.', 
                     'He feels a little embarressed.'], [3])

skellybones_ally = ally('Mr. Skellybones', 70, 100, 10,
                    [bone_blow_ally, truth_ally], [], [], [])


# ------------------------------------------------- Zeep Vorp (Ally) -------------------------------------------------

charge_ally = attack('charge', 'Proton Charge', 'Harness the power of the electromagnatism with a proton charge!', 10, 0, True, True,
                     ['It seems like Zeep Vorp remembered to set his proton charges to "Illegal everywhere except Texas" instead of "Mild Inconvience."'],
                     ['Zeep Vorp throws several proton charges at the enemies.'],
                     ['Zeep Vorp throws several proton charges at the enemies,', 'but he forgot to turn them on.', '"Vorleep zam zoop?"', 'Since he was so polite, everyone let Zeep Vorp turn on the proton charges.', '"Verleem!"', 'BOOM'],
                     ['Zeep Vorp tries to throw several proton charges but it seems like he forgot them at home.', '"Vap zeem! Jimlip?"', 'Everyone lets Zeep Vorp go back home to get them.'], [])

heal_field = attack('field', 'Heal Field', 'Heal up in this totally not FDA-approved heal field!', -15, -15, False, True,
                    ['It seems like Zeep Vorp in his clumsiness, accidentally super charged the heal field.', "He doesn't know how it happened but hey", 'if it works, it works.'],
                    ['Zeep Vorp places down a heal field.', 'Everyone feels a little bit better now, mentally and physically.'],
                    ['Zeep Vorp places down a heal field which works for a bit,', 'but he trips on it,', 'turning it off.'],
                    ['Zeep Vorp places down a heal field but he forgets the password on how to turn it on.'], [])

shield_up = attack("shield_up", "Shield Up", "Deploys a calming shield to reduce incoming damage.", 0, -10, False, False,
                   ['Zeep Vorp deploys a strangely calming shield.', 'Inside you hear oddly zen music and smell...', 'peppermint...', 'gross...', "But hey, it's the thought that counts."],
                   ['Zeep Vorp places down a shield to protect {tname}.', "{tname}'s nerves are slightly eased."],
                   ["Zeep Vorp places down a shield but it seems like he forgot the batteries, which stresses {tname} out but don't worry,", "he got it working"],
                   ['Zeep Vorp places down a shield that is not calming at all.', "It's just constant alarm clock timers going off over and over and over.", '3/10,', 'would not recommend.'],
                   [2])

zeep_vorp_ally = ally("Zeep Vorp", 60, 100, 10, [charge_ally], [shield_up],[],[heal_field])

# ------------------------------------------------- Pepper -------------------------------------------------
beam_ally = attack('beam', 'Peppermint Beam', "Don't you love it when elves do they super famous and iconic peppermint beam that everyone knows about?", 25, 0, True, False,
              ['Pepper stands back and gets ready for something.', 'She closes her eyes and starts yelling for some reason?.', 'Suddenly, she starts glowing the hat on her head turns from a dark green to a bright white.'
               '"SUPER"', '"PEPPER-"', '"MINT"', '"BEEEEEEEEEEEEAAAAAAAAAAAAAAMMMMMMMMMMM!"', 'The light from the beam is blinding.', "It's thin as paper but the damage is incredible."],
              ['Pepper makes a finger gun and points it at {tname}.','"PEPPERMINT"', '"BEAM!', "The laser blasts out of her hand and burns with the heat of a thousand suns.", "It's extremely precise and Worst of all,", 'it tastes like peppermint.', 'Gross...'],
              ['"PEPPERMINT"', '""BLAST!"', 'Nothing happens.', '"Wait..."', '"That is not right."', '"Peppermint beam?"', "The beam fires out of her hands at {tname}, but because of the embarrasment of her initial blast, it's less powerful."],
              ['PEPPERMINT', 'BEAM!', 'At the speed of light, it fires out of her hand.', 'She smirks arrogantly, proud of her actions.', 'She completely missed.', 'Haha,', 'loser.'], [])
present_ally = attack('present', 'Present', 'Use this to bug your enemies, the Christmas way.', 0, 20, True, False,
                       ['Using her elf skills,', 'Pepper quickly builds a teddy bear?', 'Huh, everyone looks at it adoringly.', 'But then, {tname} looks in its cold,', 'dead,', 'apathetic', 'eyes,', 'and is very disturbed by it.'],
                       ['Using her elf skills,', 'Pepper quickly builds a water gun and fires it at {tname}.', "Now they're cold, wet, and not very happy."],
                       ['Using her elf skills,', 'Pepper quickly builds one of those really mesmerizing fans that light up.', 'You know the one.', 'Anyway she turns it on and it mesmerizes {tname}.', '{tname} eventually regains control abd is only a little panicked to see how much happened while he was in a trance.'],
                       ['Using her elf skills,', 'Pepper quickly builds a sticky hand and flings it at {tname}.'], [])
tommy_gun = attack('tommy_gun', 'Candy Gun', "It's a gun made out of candy cane. What did you expect?", 15, 0, True, True,
                   ['PEPPER: "Heheheh!"', 'Pepper uses her gun made out of candy cane and fires indiscriminately.', 'Somehow, despite literally closing her eyes and spinning around,', 'she hits all of her shots.'],
                   ['PEPPER: "Heheheh!"' 'Pepper pulls out a tommy gun made out of candy cane and indiscriminately fires it at opponents.'],
                   ['PEPPER: "Heheheh!"', 'Pepper pelts the opponents with bullets made out of peppermint.', 'She hits them but misses most of her shots.'],
                   ['PEPPER: "Heheheh!"', 'Pepper fires her candy cane tommy gun and...', 'misses every shot!', 'You look at Pepper disappointed because she had 40 chances to hit someone and wiffed all of them.', 'PEPPER: "Can it!"', 'She says that despite you being completely silent.'], [])

pepper = ally('Pepper', 50, 100, 25, [beam_ally, present_ally, tommy_gun], [], [], [])




#if victory:
    #level_up(

    #for ally_char in allies:
       # print(ally_char)
#else:
    #'YOU LOST IDIOT!!!!!!!!'

everyone = [test_enemy, viyh, skellybones_boss, ghost, zombie_one, zombie_two, santa, agent_elf, elf_one, elf_two, reindeer, zeep_vorp_enemy, test_ally, player, skellybones_ally, zeep_vorp_ally, pepper]

# ===========================================================================================================
# =================================================== DLC ===================================================
# ===========================================================================================================

# ================================================= Items =================================================
northdakotium = item("Northdakotium", 'An ingot of Northdakotium that you have no idea what to do with.', 30, 0, False, True, [], 
                     ['You pull out your ingot of North Dakotium you had in your backpocket.', "You try to eat it for some reason but obviously that doesn't work.", "It's a slab of metal.",
                      "I don't know what you expected.", 'UNKNOWN: "Yo."', "Wait is that...", 'the ingot talking?!', 'PEPPER: "How do we use you, ingot?"', 'INGOT: "What do you mean use me?"',
                      'PEPPER: "I mean use you! Now give us something or else I\'m throwing you into a furnace."', 'INGOT: "Whoa, whoa, whoa! Let\'s not get violent here!"', 
                      'INGOT: "Look I don\'t know!"', 'You take the ingot and rub it sensually... for some reason.', 'Pepper and Mr. Skellybones avert their eyes.', 'But then the ingot starts glowing.',
                      'INGOT: "Whoa! What\'s happening to me-"', 'The ingot is converted into energy that heals you.'])

film_roll = item("Film Roll", 'A film roll containing a leaked cut of the major motion picture, "Star Jones 13: Infinitely Impossible: Part 3.6"', 0, -30, True, True, [],
                 ['You set up a film projector and a projection screen.', 'Your opponents set up the chairs and get the popcorn.', 'You, your party, and your opponents get comfortable and watch the movie.',
                  'To put it simply,', 'it was a 3 hour disgrace to the Star Jones franchise.', 'They really should have stopped after Star Jones 3.', 'Your party came out unscaved because you all already knew it would be terrible,',
                  'But fortunately, your opponents had their hopes high, and so they were disappointed.'])
# ================================================= Bosses =================================================

# ------------------------------------------------- Tutorial Fight -------------------------------------------------
gun = attack("gun", "Gun", "", 25, 0, True, False, 
             ["The robber uses his gun and misses!", "But then...", "The bullet ricochets off of the cash register and flies out of the window,", "hitting a nearby car in the tire,", 'causing the car to go wildly off course', 
              'and crash into the gas station,', 'hitting you.', 'The driver gets your insurance information and leaves.'],
             ['The robber uses his gun and hits you!'],
             ["The robber tries to use his gun but it jams.", "He throws the magazine at you instead."],
             ['The robber tries to use his gun', 'but due to the pressure of battle, he forgets how to use it.', 'He watches an online video tutorial but the thick accent makes it impossible to understand.'], [])

threat = attack("threat", "Threat", "", 0, 15, True, False,
                ["The robber points his gun at your favorite brand of chocolate.", 'ROBBER: "Um... step any closer and the chocolate gets it!"', 'You panic.'],
                ["The robber points his gun at you.", 'ROBBER: "St-stand back or I\'ll shoot!"'],
                ["The robber points his gun at you.", "He tries to fire a warning shot but he's out of ammo"],
                ["The robbber points his gun at you and drops it.", "Oops."], [])

tip = attack('tip', "Tip", '', -10, -10, False, False,
             ["The robber's mentor whispers to the robber:", 'MENTOR: "It would be kinda lame if you lost this fight."'],
             ["The robber's mentor whispers to the robber:", 'MENTOR: "If you shoot them, they will die."'],
             ["The robber's mentor whispers to the robber:", 'MENTOR: "Uh... um... honestly I do not know."', 'MENTOR: "Try to win?"'],
             ["The robber's mentor whispers to the robber.", 'But the whispering is so quiet that not even the robber understands what is said.'], [])

robber = enemy("Robber", 'Focused Damager', 80, 100, 0, [gun, threat], [], [], [])
mentor = enemy("Mentor", 'Focused Healer', 40, 100, 20, [], [], [], [tip])

# ------------------------------------------------- ND Fight -------------------------------------------------

servant = attack("servant", 'Servant Summon', '', 30, 0, True, False, 
                 ['KING: "Butler Ulbald!"', 'A extremely refined and distinguished butler magically teleports to the side of the king.', 
                  'With just a glance at the situation, the butler decides to drop kick {tname} so hard that they get sent to the slums.', 'It takes {tname} 25 minutes to walk back.', 
                  'Fortunately, everyone paused the battle until {tname} arrived', "so {tname} wouldn't miss out."],
                 ['KING: "Butler Vedlip!"', "A refined and distinguished butler rushes to the king's side.", 'KING: "Attack!"', 'The butler nods then grabs {tname}.', 
                  'He suplexes {tname} so hard that the floor below cracked.'],
                 ['KING: "Butler Ellvin!"', "A somewhat refined and distinguished butler arrives at the king's side a few minutes later.", 
                  'KING: "Attack!"', 'The butler hesitantly nods and punches {tname} in the nose.', 'He then scurries off.'],
                 ['The king tries to yell for a butler but it seems that he has lost his voice from yelling.', 'The king drinks a cup of water.'], [])

boogie = attack("dance", "Boogie", '', 0, 20, True, False, 
                ["The king challenges {tname} to a dance off.", 'The king dances so incredibly well that {tname} has no hope of winning.', '{tname} forfeits.'],
                ["The king challenges {tname} to a dance off.", "He begins but his dancing is so terrible that it made {tname} question what the point of life is."],
                ["The king challenges {tname} to a dance off.", "The king's dancing is mediocre and {tname} winces in embarassment but it's not that bad."],
                ["The king challenges {tname} to a dance off.", "The king's dancing is so incredly average that not a single soul gives a reaction."], []) 

heal_aura_enemy = attack('heal_aura', 'Heal Aura', '', -20, 0, False, True, 
                         ['The Prince tries to twist the crystal but the crystal speaks.', 'CRYSTAL: "I got you homie."', "Although only I can hear it say that because it's another inanimate voice.",
                           'Anyway, it turns itself into a neon green.', 'The healing aura that comes from it is blinding.'],
                         ['The Prince twists the crystal floating within the curve of his staff.', 'The clear crystal turns green.', 
                          'He slams the bottom of his staff down and from the crystal a healing green aura eminates.'],
                         ['The Prince twists the crystal floating within the curve of his staff.', 'The clear crystal turns red.', 'The prince then turns it again.', 
                          'It turns yellow.', 'He turns it one more time and it finally turns green and eminates a healing aura.', 'But...', 'that was the end of his turn so he sighs and stops the healing.'],
                         ['The Prince twists the crystal floating within the curve of his staff.', 'The clear crystal turns green.', 'He slams the bottom of his staff down but he slams it too hard.', 
                          'The crystal falls out of the staff and rolls to you.', 'PRINCE: "May I please have that back?"', 'You nod and hand it back.'], [])

calm_aura_enemy = attack("calm_aura", "Calming Aura", '', 0, -15, False, True,
                         ['The Prince reaches into his robe pocket and pulls out a humidifier.', 'He plugs it into a nearby outlet.', 'Since he chose the best scent,', 
                          'he and king feel way calmer.'],
                         ['The Prince twists the crystal floating in the curve of his staff.', 'The crystal turns blue.', 'He slams the staff down and a blue aura envelopes him and the king.'],
                         ['The Prince rotates the crystal too far to the right,', 'turning the pure blue closer to a turqouise color.', 'He slams the staff down but it is barely effective'],
                         ['The prince panics and forgets what angle to cast the calming spell.', 'He tries to reassure himself,', 'PRINCE: "I can do this! I just need to believe!"'], [])

king = enemy("The King of North Dakota", 'Focused Damager', 120, 100, 10, [servant, boogie], [], [], [])

prince_enemy = enemy("The Prince of North Dakota", 'AOE Healer', 50, 100, 10, [], [], [], [heal_aura_enemy, calm_aura_enemy])

king_fight = encounter([king, prince_enemy], 'dlc_dialogue/north_dakota/palace.txt', 'dlc_dialogue/north_dakota/nd_boss_victory.txt')


# ================================================= Encounters =================================================

# ------------------------------------------------- North Dakota Encounter -------------------------------------------------
spoon_stab = attack('spoon_stab', 'Spoon Stab', '', 40, 20, True, False,
                    ['The mugger does 14 spins,', '6 backflips,', '7 somersaults,', 'and then stabs {tname} with the spoon.'],
                    ['The mugger stabs {tname} with a spoon.'],
                    ['The mugger tries to stab {tname} with a spoon but somehow misses, barely grazing him.'],
                    ['The mugger tries to stab {tname} with a spoon but somehow turns 180 degrees and stabs the air.', 'The air winces in pain.'], [])

mugger_1 = enemy('Mugger 1', 'Focused Damager', 75, 75, 5, [spoon_stab], [], [], [])
mugger_2 = enemy('Mugger 2', 'Focused Damager', 75, 75, 5, [spoon_stab], [], [], [])

nd_encounter = encounter([mugger_1, mugger_2], 'dlc_dialogue/north_dakota/nd_encounter_intro.txt', 'dlc_dialogue/north_dakota/encounter_victory.txt')

# ================================================= Allies =================================================

# ------------------------------------------------- Prince of North Dakota -------------------------------------------------
heal_aura_ally = attack('heal_aura', 'Heal Aura', 'Heal everyone with this incredible non-FDA approved healing aura', -15, 0, False, True, 
                         ['The Prince tries to twist the crystal but the crystal speaks.', 'CRYSTAL: "I got you homie."', "Although only I can hear it say that because it's another disembodied voice.",
                           'Anyway, it turns itself into a neon green.', 'The healing aura that comes from it is blinding.'],
                         ['The Prince twists the crystal floating within the curve of his staff.', 'The clear crystal turns green.', 
                          'He slams the bottom of his staff down and from the crystal a healing green aura eminates.'],
                         ['The Prince twists the crystal floating within the curve of his staff.', 'The clear crystal turns red.', 'The prince then turns it again.', 
                          'It turns yellow.', 'He turns it one more time and it finally turns green and eminates a healing aura.', 'But...', 'that was the end of his turn so he sighs and stops the healing.'],
                         ['The Prince twists the crystal floating within the curve of his staff.', 'The clear crystal turns green.', 'He slams the bottom of his staff down but he slams it too hard.', 
                          'The crystal falls out of the staff and rolls to you.', 'PRINCE: "May I please have that back?"', 'Your opponent nods and hands it back.'], [])

calm_aura_ally = attack("calm_aura", "Calming Aura", "It's basically a magic humidifier, unless it's an actual humidifier", 0, -15, False, True,
                         ['The Prince reaches into his robe pocket and pulls out a humidifier.', 'He plugs it into a nearby outlet.', 'Since he chose the best scent,', 
                          'you and your party.'],
                         ['The Prince twists the crystal floating in the curve of his staff.', 'The crystal turns blue.', 'He slams the staff down and a blue aura envelopes you and your party.'],
                         ['The Prince rotates the crystal too far to the right,', 'turning the pure blue closer to a turqouise color.', 'He slams the staff down but it is barely effective'],
                         ['The prince panics and forgets what angle to cast the calming spell.', 'He tries to reassure himself,', 'PRINCE: "I can do this! I just need to believe!"'], [])

prince_ally = ally("The Prince of North Dakota", 70, 100, 30, [], [], [], [heal_aura_ally, calm_aura_ally])
# ------- Party -------
party = [player, skellybones_ally, pepper]
benched_allies = []

current_allies = party + benched_allies