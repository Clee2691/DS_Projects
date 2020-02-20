from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd


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

    start_date = '2016-03-01' # Must be in YYYY-MM-DD
    end_date = '2020-03-01' # Must be in YYYY-MM-DD

    for date in pd.date_range(start_date, end_date, freq = 'D'): # D = calendar day freq

        request_url = (
            base_url + user_id + "&dd=" + date.strftime("%Y-%m-%d")
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
