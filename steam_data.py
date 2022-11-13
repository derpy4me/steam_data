"""This module contains functions for manipulating data from Steam and visualizing it."""
# Standard Library Import
import math
from pprint import PrettyPrinter

# Third Party Imports
import pandas
from pandas import DataFrame

# Local App Imports


Printer = PrettyPrinter(indent=4)


def load_steam_data_from_file():
    return pandas.read_json(r"./most_played.json")


def get_most_played_genres(most_played: DataFrame):
    genres = most_played["genre"]
    genre_count: list[dict] = []
    for genre in genres:
        # Get list of genres from data frame.
        split_genres: list[str] = genre.split(",")
        for genre_name in split_genres:
            # For every new genre remove spaces and add a count to genre_count list.
            genre_name = genre_name.strip()
            # Make sure genre exists
            if not genre_name:
                continue

            # Iterate through existing list to see if genre already added.
            existing_dict = next((a_dict for a_dict in genre_count if a_dict["genre"] == genre_name), None)
            if not existing_dict:
                genre_count.append({"genre": genre_name, "count": 1})
            else:
                existing_dict["count"] += 1

    # Sort genres by highest count to lowest
    genre_count.sort(key=lambda a_dict: -a_dict["count"])

    return genre_count


def get_average_cost_of_most_played(most_played: DataFrame):
    cost = most_played["price"]
    # Remove NaN values
    int_cost = [int(num) for num in cost if not math.isnan(num)]
    # Return average cost rounded to 2 decimals.
    return round((sum(int_cost) / len(int_cost) / 100), 2)


def get_average_cost_per_genre(most_played: DataFrame):
    genre_details: list[dict] = []
    for _, row in most_played.iterrows():
        genres = row["genre"]
        cost = row["price"]
        if math.isnan(cost):
            cost = 0
        else:
            cost = round(cost / 100)

        split_genres = genres.split(", ")
        for genre_name in split_genres:
            genre_name = genre_name.strip()
            if not genre_name:
                continue

            existing_dict = next((a_dict for a_dict in genre_details if a_dict["genre_name"] == genre_name), None)
            if not existing_dict:
                genre_details.append({"genre_name": genre_name, "total_cost": cost, "count": 1, "average_cost": cost})
            else:
                existing_dict["total_cost"] += cost
                existing_dict["count"] += 1
                existing_dict["average_cost"] = round(existing_dict["total_cost"] / existing_dict["count"], 2)

    genre_details.sort(key=lambda a_dict: -a_dict["average_cost"])

    return genre_details


if __name__ == "__main__":
    data = load_steam_data_from_file()
    average_cost = get_average_cost_of_most_played(data)
    print(f"Average cost of most played games: {average_cost}")
    print()

    most_played_genres = get_most_played_genres(data)
    print("Most Played Genres:")
    Printer.pprint(most_played_genres)
    print()

    genre_average_costs = get_average_cost_per_genre(data)
    print("Average Genre costs:")
    Printer.pprint(genre_average_costs)
