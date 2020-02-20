from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
from pathlib import Path


def date_list_maker(year):
    """
    Makes a list of each day given the year

    arugment: Year

    Returns: list of days in YYYY-MM-DD
    """

    date_list = []

    for month in range(1, 13):
        for day in range(1, 32):
            try:
                date_list.append(datetime(year, month, day).strftime("%Y-%m-%d"))
            except ValueError:  # If day is out of range, skip it ie. no 30th of february
                pass

    return date_list


def entry_grabber(exercise_elements):
    """
    Return list of exercises from page

    Arguments: exercise_elements - html block corresponding the exercise

    return: list of exercises for specified day
    """
    log_entry_list = []

    for exercise in exercise_elements:
        # Exercise Details
        log_id = exercise.select("input[name='logid']")[0]["value"]
        exercise_id = exercise.select("input[name='exerciseid']")[0]["value"]
        exercise_name = exercise.select("input[name='ename']")[0]["value"]
        log_date = exercise.select("input[name='date']")[0]["value"]

        x = 1
        # weight and rep for each exercise
        for weight, rep in zip(
            exercise.select("input[name='weight']"),
            exercise.select("input[name='rep']"),
        ):

            set_number = x  # Specify which set number it is; not hardcoded in a value
            weight_value = weight["value"]
            rep_value = rep["value"]

            log_entry_list.append(
                [
                    log_date,
                    log_id,
                    exercise_id,
                    exercise_name,
                    set_number,
                    weight_value,
                    rep_value,
                ]
            )

            x += 1

    return log_entry_list


def csv_maker(entry):

    """
    Write the list of exercises into a csv file

    arguments: list of exercise entries

    outputs a csv file
    """

    with open("workout_list.csv", "a", newline="") as workout_file:
        writer = csv.writer(workout_file, delimiter=",")
        for data in entry:
            writer.writerow(data)


if __name__ == "__main__":

    base_url = "https://www.jefit.com/members/user-logs/log/?xid="
    user_id = "3806546"

    # specific_date = '2020-02-05' # Must be in YYYY-MM-DD

    for year in [2016, 2017, 2018, 2019, 2020]:

        date_list = date_list_maker(year)  # Make a list of dates for the year specified

        for date in date_list:
            request_url = (
                base_url + user_id + "&dd=" + date
            )  # Make the url with specified date

            user_workout = requests.get(request_url).text  # Grab HTML
            workout_html_parse = BeautifulSoup(user_workout)  # Parse HTML

            exercises_only = workout_html_parse(class_="exercise-block")

            if (
                exercises_only == []
            ):  # Empty list means no exercises for that time frame so pass
                pass
            else:
                entry = entry_grabber(exercises_only)

                if Path("workout_list.csv").is_file():  # Check if file exists
                    csv_maker(entry)

                else:
                    with open("workout_list.csv", "w+", newline="") as workout_file:
                        writer = csv.writer(workout_file, delimiter=",")
                        writer.writerow(
                            [
                                "date",
                                "log_id",
                                "exercise_id",
                                "exercise_name",
                                "set_number",
                                "weight",
                                "rep",
                            ]
                        )

                    csv_maker(entry)
