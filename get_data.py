"""This module contains functions for getting, sorting, and storing data from Steam."""
# Standard Library Import


# Third Party Imports
import pandas
import requests

# Local App Imports


def get_most_played_games():
    url = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
    response = requests.get(url, timeout=30)
    data = response.json()["response"]
    data_frame = pandas.DataFrame(data["ranks"])
    return data_frame


# def get_apps_by_id(game_ids: list[int]):
#     url = "https://api.steampowered.com/ICommunityService/GetApps/v1/?"
#     for indx, game_id in enumerate(game_ids):
#         if indx != 0:
#             url += "&"
#         url += f"appids[{indx}]={game_id}"

#     response = requests.get(url, timeout=30)

#     data = response.json()
#     print(data)


def get_apps_by_id(game_ids: list[int]):
    apps = []
    for game_id in game_ids:
        url = f"https://steamspy.com/api.php?request=appdetails&appid={game_id}"
        response = requests.get(url, timeout=30).json()
        del response["tags"]
        del response["languages"]
        apps.append(response)

    data_frame = pandas.DataFrame(apps)
    return data_frame


if __name__ == "__main__":
    most_played = get_most_played_games()
    app_details = get_apps_by_id(most_played["appid"].to_list())
    most_played = most_played.merge(app_details, how="inner", on="appid")
    most_played.to_json(r"./most_played.json")
    # read_file = pandas.read_json(r"./most_played.json")
    # print(read_file.head())
