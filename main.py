from intro_story import getStory
from funciones import run_game, prime_numbers, get_starting_airport, get_destination_airport, get_new_airport, get_distance, get_country, higher_dice, even_odd, loop_game

print(getStory())

play = input("\nEnter your name to start the game: ")

run_game(play)

if __name__ == "__main__":
    run_game(play)
