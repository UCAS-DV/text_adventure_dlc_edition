from helper_funcs import inq_select
import pygame

pygame.init()
pygame.mixer.init() 

# Converts choosen dialogue file to a list of strings
def read_dialogue_file(filepath):
    with open(filepath, 'r') as dialogue_file:
        dialogue_string = dialogue_file.read()
        dialogue = dialogue_string.split('\n')

    return dialogue

# Prints dialogue
def read_dialogue(filepath):

    print("\033c")

    # Gets dialogue string and beginning dialogue path
    dialogue = read_dialogue_file(filepath)
    audio = ''
    target_path = '1'

    for line in dialogue:
        path = line[:1]
        spot = dialogue.index(line) 

        if path == '-':
            audio = read_dialogue_file(line[1:])
            continue
        
        if path == '+':
            backing_track = line[1:]
            pygame.mixer.music.load(backing_track)
            pygame.mixer.music.play(-1)

        if path == '/':
            pygame.mixer.music.stop()

        try:
            if path == target_path and audio[spot][1:]:
                voice_line = pygame.mixer.Sound(audio[spot][1:])
                voice_line.play()
            
        except:
            pass
        
        # IF dialogue on current path, print dialogue
        if path == target_path:
            if input(f'{line[1:]} (Enter to Continue)').lower() == 'skip':
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                break

            pygame.mixer.stop()
                                                                            
        elif path == '`':
            decisions = line.split('`')

            # Present dialogue options
            while True:
                #print(f'1. {decisions[1]}')
                #print(f'2. {decisions[2]}')
                target_path = str(inq_select("which would you like to do?",decisions[1],decisions[2]))

                if target_path in ['1', '2']:
                    
                    break

def read_description(description, target):

    for line in description:
        if input(f'{line.format(tname=target.name)} (Enter to Continue)') == 'skip':
            break