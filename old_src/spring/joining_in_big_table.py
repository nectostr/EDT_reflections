"""
The script prepared to join and anonymize data
(by deleting any sensitive columns, such as name, email, etc.)
from grades table (supposed to be imported from Gauchospace)
and multiple Reflections tables (see below about rules).
Resulting table is saved to the .csv file.
"""
import os
import re

import pandas as pd


def parse_grades(filename: str, folder_path: str) -> pd.DataFrame:
    """
    The function accepts the name of the file and the path to the folder,
    reads the file, prepares columns to join and deletes the sensitive columns.
    Result of the function is a dataframe with the grades table.

    :param filename: name of the file with grades to parse (expected to be .xlsx extension)
    :param folder_path: the general path to the folder with all files
    :return: The cleaned grades table
    """
    grades_path = os.path.join(folder_path, filename)
    grades_df = pd.read_excel(grades_path, sheet_name=0)
    # grades_df = pd.read_csv(grades_path)

    grades_df["id"] = grades_df["Email address"].str.split("@").str[0]
    grades_df.drop(columns=['First name', 'Last name', 'Pronouns', 'Username', 'Email address',
           'Enroll Code', 'Perm number'], inplace=True)

    return grades_df


def parse_reflections(filename: str, folder_path: str, week_number: int) -> pd.DataFrame:
    """
    The function accepts the name of the file and the path to the folder and week number
     (to add it to prefix of all columns).
    Function reads the file, prepares columns to join and deletes the sensitive columns.
    Result of the function is a dataframe with the reflections' table from one week with columns
    "weekN_QuestionText".

    :param filename: name of the file with reflections to parse (expected to be .xlsx extension)
    :param folder_path: the general path to the folder with all files
    :param week_number:
    :return: The cleaned grades table
    """
    reflections_path = os.path.join(folder_path, filename)
    reflections_df = pd.read_excel(reflections_path)
    # reflections_df = pd.read_csv(reflections_path)

    reflections_df["id"] = reflections_df["Email Address"].str.split("@").str[0]
    reflections_df.drop(columns=['Timestamp', 'Email Address'], inplace=True)
    reflections_df.columns = [f"week{week_number}_" + col for col in reflections_df.columns]

    return reflections_df

if __name__ == "__main__":

    # TODO: Change to the folder path with reflections and grades xlsx files
    folder_path = r"data"

    # TODO: replace the name if it differs from suggestion
    grades_filename = "CMPSCW 8 - S22 Grades.egrade.xlsx"
    df = parse_grades(grades_filename, folder_path)
    print(len(df))

    # Make sure that all reflections are in the same folder and have "Reflection" and "Week N" in the name
    # Code expects them to be xlsx files
    for filename in filter(lambda x: ("Reflection" in x) and not ("Grades" in x), os.listdir(folder_path)):
        # Get current week number from name of the file
        week_number = re.findall(r"[wW]eek.*(\d+)", filename)[0]

        # Get parsed dataframe
        reflections_df = parse_reflections(filename, folder_path, week_number)
        print(filename, len(reflections_df))

        # Join the dataframe with all previous results
        df = pd.merge(df, reflections_df, left_on="id", right_on=f"week{week_number}_id", how="left")
        df.drop(columns=["week{}_id".format(week_number)], inplace=True)

    # Final anonymization
    df.drop(columns=["id"], inplace=True)

    # Save the result to the file
    df.to_csv(os.path.join(folder_path, "anonymized_results.csv"), index=False)

