import mysql.connector
import random
from geopy import distance



# Establish connection
connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='root',
    password='',
    autocommit=True
)

# Functions

def get_starting_airport():

    alku_lentoasema = "SELECT name FROM airport"
    # Initialize cursor
    cursor = connection.cursor()
    cursor.execute(alku_lentoasema)
    airports = cursor.fetchall()
    random_alku_lentoasema = random.choice(airports)
    return random_alku_lentoasema[0]

def get_destination_airport():

    loppu_lentoasema = "SELECT name FROM airport"

    cursor = connection.cursor()
    cursor.execute(loppu_lentoasema)
    airports_2 = cursor.fetchall()
    random_loppu_lentoasema = random.choice(airports_2)

    return random_loppu_lentoasema[0]


def get_distance():

    cursor = connection.cursor()

    global aeropuerto_1
    aeropuerto_1 = get_starting_airport()
    aeropuerto_2 = get_destination_airport()


    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE name=%s", (aeropuerto_1,))
    tulos = cursor.fetchone()

    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE name=%s", (aeropuerto_2,))
    tulos_2 = cursor.fetchone()

    distancia = distance.distance(tulos, tulos_2).km
    global km_available
    km_available = distancia / 2

    return f"Distance from: {aeropuerto_1} to: {aeropuerto_2} is: {distancia:.2f} km.\nYou have {km_available:.2f}km available to reach your destination.\n"


def get_country():
    cursor = connection.cursor()
    global aeropuerto_1
    cursor.execute("SELECT country.name FROM country JOIN airport ON airport.iso_country = country.iso_country WHERE airport.name=%s", (aeropuerto_1,))
    pais = cursor.fetchone()


    return pais[0]

def loop_game():
   pass


print("\nYou start at a random airport and you gotta travel to another random airport. "
      "\nYou will have available half the km of distance. "
      "\nTo earn km you can guess the country of your current airport"
      "\nor you can roll the dice."
      "\nIf you guess incorrectly you will lose 15% of your current available km."
      "\nIf you lose at dice, you will lose 10% of your current available km."
      "\nIf you guess the country you will get 15% of your current available km."
      "\nIf you win at dice, you will get 10% of your current available km."
      "\nThe game ends when you reach your destination or you run out of available km.\n"
      "\n\tGood luck!\n")

play = input("Press enter to start the game.\n")


def run_game():
    global km_available

    if play == "":

        print(get_distance())
        while True:
            opcion = int(input("Select your next move: \n1-Roll dice.\n2-Guess the country\n3-Check location\n4-Quit game\n"))
            if opcion == 1:
                dado_humano = random.randint(1, 21)
                dado_computer = random.randint(1, 21)
                puntos_dados = km_available * 0.10

                if dado_humano > dado_computer:
                    km_available = km_available + puntos_dados
                    print(f"Player wins: {dado_humano} Computer: {dado_computer}")
                    print(f"Km available: {km_available:.2f}")
                else:
                    km_available = km_available - puntos_dados
                    print(f"CPU wins: {dado_humano} player: {dado_humano}")
                    print(f"Km available: {km_available:.2f}")

            elif opcion == 2:
                puntos_pregunta = km_available * 0.15
                pais = input("Enter the country name: ")
                if pais == get_country():
                    km_available = km_available + puntos_pregunta
                    print("The country was: \n")
                    print(get_country())
                    print(f"Player wins: {km_available:.2f}")
                else:
                    km_available = km_available - puntos_pregunta
                    print("The country was: \n")
                    print(get_country())
                    print(f"CPU wins: {km_available:.2f}")

            elif opcion == 3:
                print(get_distance())

            elif opcion == 4:
                print("You lost!")
                break













if __name__ == "__main__":
    run_game()
