from math import sin, cos, sqrt, atan2, radians
from time import time
import operator


def init(departure_city_name):
    # Get the list of cities with their coordinates
    dict_cities = filter_file()
    visited_cities = []

    while True:

        # Calculate the distance of departure_city_name with the rest of the cities and returns the closest one
        nearby_city = distance_between_cities(departure_city_name, dict_cities)
        # If nearby_city is false, i save the last city of the dictionary in the visited_cities and exit the loop
        if not nearby_city:
            for k in dict_cities.keys():
                visited_cities.append(k)
            break
        # I delete the city of origin from the dictionary
        dict_cities.pop(departure_city_name)
        # I save the name of the visited city
        visited_cities.append(departure_city_name)
        # I assign the new city of origin to departure_city_name
        departure_city_name = nearby_city[0]

    return visited_cities


def filter_file():

    result = {}
    try:
        with open("cities.txt") as cities_file:
            for line in cities_file:
                # I split each line with the separator \t
                line = line.split("\t")
                city = line[0]
                latitude = line[1]
                longitude = line[2]
                # I store in a dictionary, the name of city like key and one list with the coordinates are the value
                result[city.strip()] = (latitude, longitude)
        # returns a dictionary with all cities, and his coordinates, read in the file
        return result
    except:
        print("\n\tERROR WHEN READ FILE: execution has been canceled\n")
        exit()


def calculate_distance(point1, point2):
    """taken from https://stackoverrun.com/es/q/5298235"""

    # approximate radius of earth in km
    R = 6373.0
    try:
        lat1 = radians(float(point1[0]))
        lon1 = radians(float(point1[1]))
        lat2 = radians(float(point2[0]))
        lon2 = radians(float(point2[1]))

        dif_lon = lon2 - lon1
        dif_lat = lat2 - lat1

        a = sin(dif_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dif_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return round(R * c, 2)
    except:
        print("\n\tERROR WHEN CALCULATE DISTANCE: the execution has canceled\n")
        exit()


def print_list(list1):

    for elem in list1:
        print("\t", elem)


def distance_between_cities(departure_city_name, dict_cities):
    dict_temp = {}
    # I store the coordinates from the departure_city
    departure_city_coordinates = dict_cities[departure_city_name]

    result = False
    try:
        # for each city in the dictionary,  i take the name and coordinates
        for city_name, coordinates in dict_cities.items():
            # if the city to compare is different to the departure_city
            if city_name != departure_city_name:
                # calculate the distance between them
                value_distance = calculate_distance(
                    departure_city_coordinates, coordinates
                )
                # I store the name of the city compared and the distance between them
                dict_temp[city_name] = value_distance
                # I sort the result based on distance and store the first element in dictionary
                result = sorted(
                    dict_temp.items(), key=operator.itemgetter(1), reverse=False
                )[0]
    finally:
        return result


start_time = time()

departure_city_name = "Beijing"
visited_cities = init(departure_city_name)
print_list(visited_cities)

elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)
