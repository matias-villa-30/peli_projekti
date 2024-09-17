import mysql.connector
import random
import math
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

# SQL functions

def alter_foreign_key():
    cursor = connection.cursor()
    try:
        # Replace 'constraint_name' with the actual foreign key constraint name
        cursor.execute("ALTER TABLE goal_reached DROP FOREIGN KEY constraint_name1")
        cursor.execute("ALTER TABLE goal DROP FOREIGN KEY constraint_name2")
        cursor.execute("ALTER TABLE game DROP FOREIGN KEY constraint_name3")

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

    finally:
        cursor.close()
def drop_table():
    cursor = connection.cursor()
    try:
        cursor.execute('DROP TABLE IF EXISTS game')
        cursor.execute('DROP TABLE IF EXISTS goal')
        cursor.execute('DROP TABLE IF EXISTS goal_reached')

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()

    finally:
        cursor.close()



# Functions for mini games

def prime_numbers(dice):
    global km_available
    global distancia
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

def get_starting_airport():

    alku_lentoasema = "SELECT name FROM airport"

    cursor = connection.cursor()
    cursor.execute(alku_lentoasema)
    airports = cursor.fetchall()
    global random_alku_lentoasema
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
    global tulos

    cursor.execute("SELECT name FROM airport WHERE latitude_deg <= %s AND longitude_deg <= %s", (tulos[0], tulos[1]))
    nuevo_aeropuerto = cursor.fetchone()
    aeropuerto_1  = nuevo_aeropuerto
    return f"You were gifted a ticket to: {nuevo_aeropuerto[0]}"

def points_deducted():
    global km_available
    puntos = km_available * 0.25
    km_available = km_available - puntos
    return f"You lost: {puntos:.2f} km and you now have: {km_available:.2f} km available."

def points_gained():
    global km_available
    puntos = km_available * 0.15
    km_available = km_available + puntos
    return f"You won:  {puntos:.2f} km and you now have: {km_available:.2f} km available."

def get_country():
    cursor = connection.cursor()
    global aeropuerto_1
    cursor.execute("SELECT country.name FROM country JOIN airport ON airport.iso_country = country.iso_country WHERE airport.name=%s", (aeropuerto_1,))
    pais = cursor.fetchone()

    return pais[0]

def even_odd(par_impar):
    global km_available
    global distancia
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

def get_airport_height():
    cursor = connection.cursor()
    global aeropuerto_1
    cursor.execute("SELECT elevation_ft FROM airport WHERE name=%s", (aeropuerto_1,))
    global altura
    altura = cursor.fetchone()

    return altura[0]

def get_location():
    cursor = connection.cursor()
    global aeropuerto_1
    cursor.execute("SELECT municipality FROM airport WHERE name=%s", (aeropuerto_1,))
    location = cursor.fetchone()
    return location[0]


def higher_dice(dado):
    global km_available
    global distancia
    dado_humano = random.randint(1, 21)
    dado_computer = random.randint(1, 21)

    if dado_humano > dado_computer:

        print(f"Player wins: {dado_humano} Computer: {dado_computer}")
        print(points_gained())
    else:

        print(f"CPU wins: {dado_humano} player: {dado_humano}")
        print(points_deducted())

def guess_country(pais):

    print(f"You are at: {aeropuerto_1}")

    if pais.lower() == get_country():
        print(points_gained())
        print(get_new_airport())

    else:
        print(points_deducted())


def loop_game():

    global km_available
    global distancia

    print(get_distance())

    while km_available > 0:
        if km_available >= distancia:
            print("You won!\n You can now reach your destination.\n Congratulations!")
            break

        elif km_available <= 0:
            print("You lost!")
            break

        opcion = int(input("Select your next move: \n1-Roll dice\n2-Guess airport information\n3-Check location and distance\n4-Quit game\n"))

        if opcion == 1:
            juego = int(input("Select minigame: \n1-Higher roll\n2-Even or odd.\n3-Prime number or not\n"))

            if juego == 1:
                higher_dice(juego)

            elif juego == 2:
                player_input = input("Even or odd: ")
                even_odd(player_input)

            elif juego == 3:
               serku = input("Prime number. yes or no:\n")
               prime_numbers(serku)

            else:
                print("Invalid input")

        elif opcion == 2:

            peli = int(input("Select minigame: \n1-Guess the country.\n2-Guess the elevation.\n3-Guess the location\n"))

            if peli == 1:
                global aeropuerto_1
                print(f"A reminder of your location: {aeropuerto_1}")
                pais = input("Enter the country name: ")
                guess_country(pais)

            elif peli == 2:

                height = int(input("Enter the height of your airport: "))
                if height == get_airport_height():
                    print(points_gained())
                    print(get_new_airport())
                else:
                    print(points_deducted())
                    print(get_new_airport())

            elif peli == 3:
                localidad = input("Enter the municipality name: ")
                if localidad.lower() == get_location():
                    print(points_gained())
                else:
                    print(points_deducted())


        elif opcion == 3:
            print(f"Your current location is: {aeropuerto_1}\nYou have: {km_available:.2f} km available.")

        elif opcion == 4:
            print("You lost!")
            break




