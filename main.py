from intro_story import getStory
from funciones import run_game

print(getStory())

play = input("\nEnter your name to start the game: ")

if __name__ == "__main__":
    run_game(play)
