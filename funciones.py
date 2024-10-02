import mysql.connector
import random
import math
from mysql.connector import errors
from geopy import distance


connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='root',
    password='',
    autocommit=True
)

# Database functions


# Handle errors
def clear_unread_results():
    try:
        cursor = connection.cursor()

        while cursor.nextset():
            cursor.fetchall()
    except mysql.connector.Error as e:

        pass

# Functions for dice mini games
def higher_dice(dado):

    dado_humano = random.randint(1, 21)
    dado_computer = random.randint(1, 21)

    if dado_humano > dado_computer:

        print(f"Player wins: {dado_humano} Computer: {dado_computer}")
        print(points_gained())
    else:

        print(f"CPU wins: {dado_humano} player: {dado_humano}")
        print(points_deducted())

def even_odd(par_impar):

    dado = random.randint(1, 21)
    if par_impar.lower() == "even" and dado % 2 == 0:
        print(points_gained())

    elif par_impar.lower() == "odd" and dado % 2 != 0:
        print(points_deducted())

    elif par_impar.lower() != "even" and par_impar.lower() != "odd":
        print("Wrong input, back to main menu")

    else:
        print(f"Result is: {dado}")
        print(points_deducted())

def prime_numbers(dice):

    alkuluku = random.randint(1, 21)
    on_alkuluku = True

    for i in range(2, int(math.sqrt(alkuluku)) + 1):
        if alkuluku % i == 0:
            on_alkuluku = False


    if dice.lower() == "yes" and on_alkuluku == True:
        print(f"{alkuluku} is a prime number!")
        print(points_gained())

    elif dice.lower() == "no" and on_alkuluku == False:
        print(f"{alkuluku} is not a prime number!")
        print(points_gained())

    elif dice.lower() == "yes" and on_alkuluku == False:
        print(f"{alkuluku} is not a prime number.")
        print(points_deducted())

    elif dice.lower() == "no" and on_alkuluku == True:
        print(f"{alkuluku} is a prime number.")
        print(points_deducted())

# Point system


global km_lost
global km_won
km_lost = 0
km_won = 0

def points_deducted():
    global loss
    global km_available
    global km_lost

    puntos = km_available * 0.25
    km_lost += puntos
    km_available = km_available - puntos
    loss += 1
    return f"You lost: {puntos:.2f} km and you now have: {km_available:.2f} km available."

def points_deducted2():
    global loss
    global km_available
    global km_lost

    puntos = km_available * 0.40
    km_lost += puntos
    km_available = km_available - puntos
    loss += 1
    return f"You lost: {puntos:.2f} km and you now have: {km_available:.2f} km available."

def points_gained():
    global voito
    global km_available
    global km_won

    puntos = km_available * 0.15
    km_won += puntos
    km_available = km_available + puntos
    voito += 1
    return f"You won: {puntos:.2f} km and you now have: {km_available:.2f} km available."

def points_gained_2():
    global voito
    global km_available
    global km_won
    puntos = km_available * 0.40
    km_available = km_available + puntos
    km_won += puntos
    voito += 1
    return f"You won: {puntos:.2f} km and you now have: {km_available:.2f} km available."

# Functions for airport locations and distance

def get_starting_airport():
    cursor = connection.cursor()
    global random_alku_lentoasema
    global aeropuertos_visitados
    aeropuertos_visitados = []

    alku_lentoasema = "SELECT name FROM airport WHERE type = 'large_airport'"

    while True:
        try:
            cursor.execute(alku_lentoasema)
            airports = cursor.fetchall()
            random_alku_lentoasema = random.choice(airports)
            aeropuertos_visitados.append(random_alku_lentoasema[0])
            return random_alku_lentoasema[0]

        except errors.InternalError as e:
            if "Unread result found" in str(e):
                cursor.fetchall()
            else:
                raise e
        except mysql.connector.Error as err:
            raise err

def get_destination_airport():
    loppu_lentoasema = "SELECT name FROM airport WHERE type = 'large_airport'"
    cursor = connection.cursor()
    cursor.execute(loppu_lentoasema)
    airports_2 = cursor.fetchall()
    random_loppu_lentoasema = random.choice(airports_2)

    return random_loppu_lentoasema[0]

def get_distance():
    clear_unread_results()
    cursor = connection.cursor()
    global aeropuerto_1
    aeropuerto_1 = get_starting_airport()
    aeropuerto_2 = get_destination_airport()

    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE name=%s", (aeropuerto_1,))
    global tulos
    tulos = cursor.fetchone()

    cursor.execute("SELECT latitude_deg, longitude_deg FROM airport WHERE name=%s", (aeropuerto_2,))

    tulos_2 = cursor.fetchone()

    global distancia
    distancia = distance.distance(tulos, tulos_2).km
    global km_available
    km_available = distancia / 2

    return f"Distance from: {aeropuerto_1} to: {aeropuerto_2} is: {distancia:.2f} km.\nYou have {km_available:.2f} km available to reach your destination.\n"

def get_new_airport():
    cursor = connection.cursor()
    global aeropuerto_1
    global distancia
    global aeropuertos_visitados
    cursor.execute("SELECT name FROM airport WHERE type = 'large_airport'")
    nuevo_aeropuerto = cursor.fetchall()

    random_nuevo = random.choice(nuevo_aeropuerto)
    aeropuerto_1  = random_nuevo[0]
    aeropuertos_visitados.append(aeropuerto_1)


    return f"You were gifted a ticket to: {aeropuerto_1}"

# Functions for airport minigames
def get_country():
    cursor = connection.cursor()
    global pais
    global play
    global aeropuerto_1
    cursor.execute("SELECT country.name FROM country JOIN airport ON airport.iso_country = country.iso_country WHERE airport.name=%s", (aeropuerto_1,))
    pais = cursor.fetchone()

    return pais[0]


def get_airport_height():
    clear_unread_results()
    cursor = connection.cursor()
    global aeropuerto_1
    cursor.execute("SELECT elevation_ft FROM airport WHERE name=%s", (aeropuerto_1,))
    global altura
    altura = cursor.fetchone()

    return altura[0]

def get_location():
    clear_unread_results()
    cursor = connection.cursor()
    global aeropuerto_1
    cursor.execute("SELECT municipality FROM airport WHERE name=%s", (aeropuerto_1,))
    location = cursor.fetchone()
    return location[0]

# RUN GAME

def insert_airport_data():
    global play
    global aeropuertos_visitados
    cursor = connection.cursor()
    # Example list of airports visited

    # Prepare the data for insertion (e.g., all rows associated with a specific player)
    data = [(play, airport) for airport in aeropuertos_visitados]

    # Use executemany to insert all rows at once
    cursor.executemany("INSERT INTO stats_airport (player_name, airports_visited) VALUES (%s, %s)", data)
    connection.commit()  # Commit the changes

def insert_minigame_data():
    global play, voito, loss, km_won, km_lost
    cursor = connection.cursor()
    cursor.execute("INSERT INTO stats_minigames (player_name, minigames_won, minigames_lost, km_won, km_lost) VALUES (%s, %s, %s, %s, %s)", (play, voito, loss, km_won, km_lost))
    connection.commit()  # Commit the changes

def loop_game():
    global aeropurtos_visitados
    global voito
    global loss
    global km_available
    global distancia
    global games_won
    global aerpuerto_1
    loss = 0
    voito = 0
    games_won = 0
    games_lost = 0
    print(get_distance())

    while True:


        opcion = input("Select your next move: \n1-Roll dice\n2-Guess airport information\n3-Check location and distance\n4-Quit game\n")



        if opcion < "0" or opcion > "4":
            print("Invalid input")

        if opcion == "4":
            print("You lost!")
            games_lost += 1
            insert_airport_data()
            insert_minigame_data()
            break

        if opcion == "1":

            juego = input("Select minigame: \n1-Higher roll\n2-Even or odd.\n3-Prime number or not\n")

            if juego == "1":
                higher_dice(juego)

            elif juego == "2":
                player_input = input("Even or odd: ")
                even_odd(player_input)

            elif juego == "3":
               serku = input("Prime number. yes or no:\n")
               prime_numbers(serku)

            else:
                print("Invalid input")

        elif opcion == "2":
            peli = input("Select minigame: \n1-Guess the country.\n2-Guess the elevation.\n3-Guess the location\n")

            if peli == "1":
                global aeropuerto_1
                global aeropuerto_2
                global aeropuertos_visitados
                print(f"A reminder of your location: {aeropuerto_1}")

                pais = input("Enter the country name: ")
                if pais.lower() == get_country().lower():
                    print(points_gained_2())
                    print(get_new_airport())
                else:
                    print(points_deducted2())

            elif peli == "2":
                print(f"A reminder of your location: {aeropuerto_1}")
                height = int(input("Enter the height of your airport: "))
                if height == get_airport_height():
                    print(points_gained_2())
                    print(get_new_airport())
                else:
                    print(points_deducted())

            elif peli == "3":
                print(f"A reminder of your location: {aeropuerto_1}")

                localidad = input("Enter the municipality name: ")
                if localidad.lower() == get_location().lower():
                    print(points_gained_2())
                    print(get_new_airport())
                else:
                    print(points_deducted())


        elif opcion == "3":
            print(f"Your current location is: {aeropuerto_1}\nYou have: {km_available:.2f} km available.")

        if km_available <= 50:
            print("You lost!")
            games_lost += 1
            insert_airport_data()
            insert_minigame_data()
            break

        if km_available >= distancia:
            print("You won!\nYou can now reach your destination.\nCongratulations!")
            games_won += 1
            insert_airport_data()
            insert_minigame_data()
            break


def run_game():
    global play
    play = input("\nEnter your name to start the game: ")


    loop_game()


