import json
import time
from datetime import datetime, timedelta
import argparse
import os

def check_translation_fields(translation_data: dict) -> str:
    """
    This function checks if each translation dictionary have the expected key name and value type.

    Parameters:
        translation_data (dict): A dictionary of each translation information.

    Returns:
        boolean: A flag that indicates if the sample has the expected format.
    """
    # Expected keys to be in the dictionaries
    expected_keys= [
        "timestamp",
        "translation_id",
        "source_language",
        "target_language",
        "client_name",
        "event_name",
        "nr_words",
        "duration"
    ]

    # Types of the expected keys
    expected_types= [
        str,
        str,
        str,
        str,
        str,
        str,
        int,
        int
    ]

    variables_types = list(zip(expected_keys, expected_types))

    # Check all fields from the translation and see if one is not expected 
    for key in translation_data.keys():
        if key not in expected_keys:
            raise Exception(f"""Field "{key}" is not expected in the translation data. Please correct input.""")
    
    # Check if all mandatory fields are on the file 
    for key in expected_keys:
        if key not in translation_data.keys():
            raise Exception(f"""Field "{key}" is missing in the translation data. Please correct the input.""")
    
    # If translation has all the correct fields, will check if the fields have the expected types
    for key, expected_type in variables_types:
        value = translation_data[key]
        if not isinstance(value, expected_type):
            raise Exception(f"""Type of the field "{key}" is not the expected one: received "{type(value)}", expected "{expected_type}".""")
        
    return True

def pars_translation_files(file_path: str) -> list[dict]:
    """
    Reads input file containing the translations information, parse it and returns a list with a dictionary
    for each translation delivered. Also, it removes duplicated translations(same translation id).

    Parameters:
        file _path (str): Path to the json file containing information for each translation.

    Returns:
        list[dict]: List with a dictionary for each translation.
    """

    loaded_translations:list = []
    processed_translations = []

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"""File "{file_path}" not found. Insert an existing one.""")

    # Open the JSON file
    with open(file_path, "r") as file:
        for line in file:
            data = json.loads(line)
            # If the format of the translation is not correct, raises an Exception and stops the script.
            # If it is correct, proceeds.
            correct_format = check_translation_fields(data)
            if correct_format:
                # If it is not a duplicated translation
                if data["translation_id"] not in processed_translations:
                    # Append translation to the loaded_transaltions list and add the id to the already processed list
                    loaded_translations.append(data)
                    processed_translations.append(data["translation_id"])
                    try:
                        # Transform the timestamp string into a datetime.datetime type in order to facilitate the manipulation of data.
                        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        raise ValueError("Timestamp field must be in this format: Year-Month-Day Hours:Minutes:Seconds:Microseconds. \nCorrect the file.")
    
    return loaded_translations

def create_list_of_minutes(data: list[dict]) -> list:
    """
    This function receives the list with the translations information and returns a list
    with the sequence of minutes, from the oldest timestamp to the most recent.

    Parameters:
        data (list[dict]): A list with the information of each translation.
    
    Return:
        list: A list with the sequence of timestamps.
    """ 
    # Since data comes ordered from the oldest to the most recent, the minimum timestamp is from the first translation and the maximum
    # timestamp is from the last translation.

    # The minimum date is the timestamp from the first translation record rounded to the minutes
    min_time = data[0]["timestamp"].replace(second=0, microsecond=0)

    # The maximum date is the timestamp from the last translation rounded to the minutes plus one.
    max_time=data[-1]["timestamp"].replace(second=0, microsecond=0) + timedelta(minutes=1)

    list_of_minutes = []
    current_time = min_time

    # Check if file is ordered in the expected way: from the latest to most recent translation
    if min_time > max_time:
        raise Exception(
            "File must be ordered from the latest translation to the most recent, please correct the input file."
        )

    # Adds the minimum time to a list and then increment the timestamp minute by minute until the maximum timestamp is reached and saved 
    while current_time <= max_time:
        list_of_minutes.append(current_time)
        current_time += timedelta(minutes=1)

    return list_of_minutes

def calc_moving_average(list_of_minutes: list, data: list[dict], window_size: int) -> list[dict]:
    """
    Receives a list with a sequence of minutes and computes for each timestamp the moving average of the duration
    for the last <window_size> minutes. 
    
    Parameters:
        list_of_minutes (list): list with the sequence of timestamps.
        data (list[dict]): list containing the information of each translation.
        window_size (int): the number of minutes to be considered in the moving average.
    
    Return:
        list[dict]: list with the moving average of the translations" duration for each timestamp.

    """
    if window_size <= 0:
        raise Exception("Window size value must be greater than 0.")

    avg_delivery=[]

    # Iterates through each timestamp in the sequence of timestamps
    for minute in list_of_minutes:

        mv_avg = {}
        samples_counter = 0
        mv_avg["date"]=minute 
        total_duration=0

        for data_register in data:
            # If the data's timestamp is greater than the minute in analysis there is no need to check the following translations,
            # since it is known that the timestamp will keep increasing
            if data_register["timestamp"] > minute:
                total_duration += 0
                mv_avg["average_delivery_time"]=total_duration
                break
            else:
                # For each translation, checks if the timestamp is inside the window size of the current minute
                if (minute-timedelta(minutes=window_size) <= data_register["timestamp"] <= minute):
                    # If yes, adds the duration of the translation and increments the counter to compute the current average delivery time
                    total_duration += data_register["duration"]
                    mv_avg["average_delivery_time"]=total_duration
                    samples_counter += 1
                else:
                    # If the duration is not inside the window size, add zero to the total duration
                    total_duration += 0
                    mv_avg["average_delivery_time"]=total_duration
    
        # Compute the moving average value by dividing the total duration by the total number of samples
        if samples_counter != 0:
            mv_avg["average_delivery_time"] = mv_avg["average_delivery_time"]/samples_counter

        # Transform timestamp into a more readable format
        mv_avg["date"] = datetime.strftime(mv_avg["date"], "%Y-%m-%d %H:%M:%S") 

        avg_delivery.append(mv_avg)

    return avg_delivery

def save_output_file(data: list[dict]) -> None:
    """
    Receives as input the list of dictionaries and saves it in a json file.

    Parameters:
        data (list[dict]): list with a dictionary for each timestamp moving average.
    """
    # Path to save the JSON file
    json_file_path = "output_file.json"

    # Save the list of dictionaries to a JSON file
    with open(json_file_path, "w") as json_file:
        for dictionary in data:
            json.dump(dictionary, json_file)
            json_file.write("\n") 

def main():
    """
    Define main script
    """
    # Define the arguments to define when calling for the script
    parser = argparse.ArgumentParser(
        description="Insert necessary arguments to compute the moving average for each timestamp", 
        epilog="Thank you :)"
    )
    parser.add_argument("path", type=str, help="Path to the input file contaning the translations information")
    parser.add_argument("window_size", type=int, help="Size of the window to be considered in the moving average")

    args = parser.parse_args()

    # Build main workflow   
    parsed_data = pars_translation_files(args.path)
    list_of_minutes = create_list_of_minutes(parsed_data)
    moving_average_list = calc_moving_average(list_of_minutes, parsed_data, args.window_size)
    save_output_file(moving_average_list)

if __name__ == "__main__":
    main()