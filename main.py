import mysql.connector
import random
from geopy import distance


def dados():
    dado_pelaaja = random.randint(1, 21)
    dado_cpu = random.randint(1, 21)
    return f"Sinun tulos on: {dado_pelaaja}\nCPU tulos on: {dado_cpu}"
# Establish connection
connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='peli_projekti',
    user='root',
    password='',
    autocommit=True
)
print("You start at a random airport and you gotta travel to another random airport. \nYou will have available half the km of distance. \nTo earn km you can roll a dice and beat an algorithm\n")
cursor = connection.cursor()
play = input("Press enter to start the game.")

if play == "":
    # Query to get all airport names
    airport_query = "SELECT ident, name, latitude_deg, longitude_deg FROM airport"
    cursor.execute(airport_query)
    airport_results = cursor.fetchall()

    if airport_results:
        # Choose a random starting airport
        random_airport_1 = random.choice(airport_results)
        print(f"Olet tässä: {random_airport_1[1]}")

        # Query to get the corresponding country name for the selected airport
        country_query_1 = """
        SELECT country.name 
        FROM country 
        JOIN airport ON airport.iso_country = country.iso_country
        WHERE airport.name = %s
        """
        cursor.execute(country_query_1, (random_airport_1[1],))
        country_result_1 = cursor.fetchone()

        if country_result_1:
            print(f"Mää on: {country_result_1[0]}\n")

        # Get the coordinates of the first airport
        coords_1 = (random_airport_1[2], random_airport_1[3])  # latitude_deg, longitude_deg

    # Choose a random destination airport
    if airport_results:
        random_airport_2 = random.choice(airport_results)
        print(f"Sinun pitää mennä: {random_airport_2[1]}")

        # Query to get the corresponding country name for the second airport
        country_query_2 = """
        SELECT country.name 
        FROM country 
        JOIN airport ON airport.iso_country = country.iso_country
        WHERE airport.name = %s
        """
        cursor.execute(country_query_2, (random_airport_2[1],))
        country_result_2 = cursor.fetchone()

        if country_result_2:
            print(f"Mää on: {country_result_2[0]}\n")

        # Get the coordinates of the second airport
        coords_2 = (random_airport_2[2], random_airport_2[3])  # latitude_deg, longitude_deg

        # Calculate the distance between the two airports
        välimatka = distance.distance(coords_1, coords_2).km
        print(f"Välimatka on: {välimatka:.2f} km")
        km_available = välimatka / 2
        print(f"Sinulla on {km_available:.2f} km käytössä")

    # Option to show nearby airports
    opciones = int(input("\nSinä voit: \n1-Matkustaa\n2-Valita peli\n"))
    if opciones == 1:
        # Select airports where the distance is less than or equal to km_available
        nearby_airports = []
        for airport in airport_results:
            airport_coords = (airport[2], airport[3])  # latitude_deg, longitude_deg of each airport
            välimatka_airport = distance.distance(coords_1, airport_coords).km

            if välimatka_airport <= km_available and airport[0] != random_airport_1[0]:
                nearby_airports.append((airport[1], välimatka_airport))

        # Randomly pick up to 10 nearby airports
        a = 1
        if nearby_airports:
            limited_nearby_airports = random.sample(nearby_airports, min(10, len(nearby_airports)))

            print("\nLähellä olevat lentoasemat: ")
            for airport_name, dist in limited_nearby_airports:


                print(f"{a}){airport_name}: {dist:.2f} km")
                a += 1
        else:
            print("Ei lentoasemia lähellä.")

    if opciones == 2:
        print(dados())


# Close the cursor and connection
cursor.close()
connection.close()
