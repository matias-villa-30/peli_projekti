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

# Functions

def prime_numbers(dice):
    global km_available
    global distancia
    alkuluku = random.randint(1, 21)
    on_alkuluku = True

    for i in range(2, int(math.sqrt(alkuluku)) + 1):
        if alkuluku % i == 0:
            on_alkuluku = False


    if dice.lower() == "yes" and on_alkuluku == True:
        puntos_primo = km_available * 0.10
        km_available = km_available + puntos_primo
        print(f"{alkuluku} is a prime number! You won: {puntos_primo:.2f}, you now have {km_available:.2f} km available.")

    elif dice.lower() == "no" and on_alkuluku == False:
        puntos_primo = km_available * 0.10
        km_available = km_available + puntos_primo
        print(f"{alkuluku} is not a prime number! You won: {puntos_primo:.2f}, you now have {km_available:.2f} km available.")

    elif dice.lower() == "yes" and on_alkuluku == False:
        puntos_primo = km_available * 0.10
        km_available = km_available - puntos_primo
        print(f"{alkuluku} is not a prime number. You lost: {puntos_primo:.2f}, you now have {km_available:.2f} km available.")

    elif dice.lower() == "no" and on_alkuluku == True:
        puntos_primo = km_available * 0.10
        km_available = km_available - puntos_primo
        print(f"{alkuluku} is a prime number. You lost: {puntos_primo:.2f}, you now have {km_available:.2f} km available.")


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

    global distancia
    distancia = distance.distance(tulos, tulos_2).km
    global km_available
    km_available = distancia / 2

    return f"Distance from: {aeropuerto_1} to: {aeropuerto_2} is: {distancia:.2f} km.\nYou have {km_available:.2f} km available to reach your destination.\n"

def get_new_airport():
    pass


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
        puntos_dados = km_available * 0.10
        km_available = km_available + puntos_dados
        print(f"Result is: {dado}")
        print(f"You won {puntos_dados:.2f} points. Your current km available is {km_available:.2f}")
    elif par_impar.lower() == "odd" and dado % 2 != 0:
        puntos_dados = km_available * 0.10

        km_available = km_available + puntos_dados
        print(f"Result is: {dado}")
        print(f"You won {puntos_dados:.2f} points. Your current km available is {km_available:.2f}")
    elif par_impar.lower() != "even" and par_impar.lower() != "odd":
        print("Wrong input, back to main menu")
    else:
        puntos_dados = km_available * 0.10

        km_available = km_available - puntos_dados
        print(f"Result is: {dado}")
        print(f"You lost {puntos_dados:.2f} points. Your current km available is {km_available:.2f}")


def higher_dice(dado):
    global km_available
    global distancia
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

def loop_game():
    global km_available
    global distancia

    print(get_distance())
    while km_available > 0 or km_available < distancia:
        opcion = int(input(
            "Select your next move: \n1-Roll dice.\n2-Guess the country\n3-Check location and distance\n4-Quit game\n"))
        if opcion == 1:
            juego = int(input("Select minigame: \n1-Higher roll.\n2-Even or odd.\n3-Prime number or not\n"))
            if juego == 1:
                higher_dice(juego)

            elif juego == 2:
                player_input = input("Even or odd: ")
                even_odd(player_input)

            elif juego == 3:
               serku = input("Prime number. yes or no:\n")
               prime_numbers(serku)





        elif opcion == 2:

            puntos_pregunta = km_available * 0.15
            print(f"You are at: {aeropuerto_1}")
            pais = input("Enter the country name: ")
            if pais.lower() == get_country().lower():

                km_available = km_available + puntos_pregunta
                print(f"Nice! You won {puntos_pregunta:.2f} points. The country was: ")
                print(get_country())
                print(f"You now have: {km_available:.2f} km available.")
            else:
                km_available = km_available - puntos_pregunta
                print(f"Wrong! You lost {puntos_pregunta:.2f} points.")
                print(f"You now have: {km_available:.2f} km available.")

        elif opcion == 3:
            print(f"Your current location is: {aeropuerto_1}\nYou have: {km_available:.2f} km available.")

        elif opcion == 4:
            print("You lost!")
            break

        if km_available == 0:
            print("You lost!\nYou are out of km")
            break

        elif km_available == distancia:
            print("You won!\n You can now reach your destination.\n Congratulations!")