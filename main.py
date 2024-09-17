from funciones import prime_numbers, get_starting_airport, get_destination_airport, get_new_airport, get_distance, \
    get_country, higher_dice, even_odd, loop_game, guess_country, drop_table, alter_foreign_key

print("\nYou start at a random airport and you gotta travel to another random airport. "
      "\nYou will have available half the km of distance. "
      "\nTo earn km you can guess the country of your current airport"
      "\nor you can roll the dice and play different dice mini games."
      "\nIf you guess incorrectly you will lose 15% of your current available km."
      "\nIf you lose at dice, you will lose 10% of your current available km."
      "\nIf you guess the country you will get 15% of your current available km."
      "\nIf you win at dice, you will get 10% of your current available km."
      "\nIf you guess the country correctly, you will sent to a different random airport within your reach"
      "\nThe game ends when you earned enough km to reach your destination or you run out of available km.\n"
      "\n\tGood luck!\n")

play = input("Enter your name to start the game: ")


def run_game():

    if play.lower():
        loop_game()


if __name__ == "__main__":
    run_game()
