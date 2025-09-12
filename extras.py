from helper_funcs import inq_select
from image_loader import display_image
from inspect_character import get_char_stats
from game_assets import everyone
def extras_main():
    while True:
        choice = inq_select("View:", "Unused Inspect Characters", "Exit")

        match choice:
            case 1:
                selection = inq_select("Which charecter would you like to inspect?", *everyone)
                selection = everyone[selection-1]
                get_char_stats(selection)
            case 2:
                break


    
if __name__ == "__main__":
    extras_main()
#extras_main()
