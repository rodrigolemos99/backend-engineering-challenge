import pytest
import json
from datetime import datetime, timedelta

import unbabel_cli as mv_avg_script

# This script has the main objective to confirm that the implemented python functions to compute the moving average 
# of the translations's duration work as expected.

# Pytest fixtures are inputs for the test functions. The goal is to reutilize this fixtures instead of creating equal inputs for every test.

@pytest.fixture
def dummy_list_of_dicts():
    """
    Creates a list of dictionaries to use in the tests.
    First dict: incorrect field.
    Second dict: incorrect type.
    Third dict: missing mandatory field.
    Fourth dict: correct input
    """

    sample_data = [
        {"time_stamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20},
        {"timestamp": "2018-12-26 18:15:19.903159","translation_id": 87483, "source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31},
        {"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100},
        {"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20},
    ]

    return sample_data

@pytest.fixture
def dummy_correct_translation():
    """
    Creates a dummy list with the expected format of the output of function pars_translation_files. 
    """
    sample_data = [
        {"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20},
        {"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31},
        {"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54},
    ]  

    new_sample = []

    for sample in sample_data:
        sample["timestamp"] = datetime.strptime(sample["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        new_sample.append(sample)

    return new_sample    

@pytest.fixture
def dummy_list_of_minutes():
    """
    Return an ordered list of minutes.
    """
    expected_list = [
        datetime(2018, 12, 26, 18, 11),
        datetime(2018, 12, 26, 18, 12),
        datetime(2018, 12, 26, 18, 13),
        datetime(2018, 12, 26, 18, 14),
        datetime(2018, 12, 26, 18, 15),
        datetime(2018, 12, 26, 18, 16),
        datetime(2018, 12, 26, 18, 17),
        datetime(2018, 12, 26, 18, 18),
        datetime(2018, 12, 26, 18, 19),
        datetime(2018, 12, 26, 18, 20),
        datetime(2018, 12, 26, 18, 21),
        datetime(2018, 12, 26, 18, 22),
        datetime(2018, 12, 26, 18, 23),
        datetime(2018, 12, 26, 18, 24),
    ]
    return expected_list


# Here start the tests for function check_translation_fields.

def test_check_translation_fields(dummy_list_of_dicts):
    """
    Test if function check_translation_fields is working correctly. If the input is formated correctly,
    the function output is a boolean True.
    """
    assert mv_avg_script.check_translation_fields(dummy_list_of_dicts[3]) is True


def test_check_translation_fields_incorrect_field(dummy_list_of_dicts):
    """
    Test if function check_translation_fields handles an input with a dictionary key different from the
    expected ones.
    """
    with pytest.raises(Exception) as inc_key:
        mv_avg_script.check_translation_fields(dummy_list_of_dicts[0])

    assert(
        str(inc_key.value) == """Field "time_stamp" is not expected in the translation data. Please correct input."""
    )


def test_check_translation_fields_incorrect_type(dummy_list_of_dicts):
    """
    Test if function check_translation_fields handles an input with an incorrect key type.
    """
    with pytest.raises(Exception) as inc_type:
        mv_avg_script.check_translation_fields(dummy_list_of_dicts[1])

    assert(
        str(inc_type.value) == """Type of the field "translation_id" is not the expected one: received "<class 'int'>", expected "<class 'str'>"."""
    )


def test_check_translation_fields_missing_field(dummy_list_of_dicts):
    """
    Test if function check_translation_fields handles an input with a missing dicitonary key.
    """
    with pytest.raises(Exception) as miss_key:
        mv_avg_script.check_translation_fields(dummy_list_of_dicts[2])

    assert(
        str(miss_key.value) == """Field "duration" is missing in the translation data. Please correct the input."""
    )


# Here start the tests for function pars_translation_files.

def test_pars_translation_files(dummy_correct_translation):
    """
    Test if pars_translation_files function works as expected, creating a list of dictionaries and converting timestamp
    from string to datetime.datetime.
    """
    parsed_file = mv_avg_script.pars_translation_files("tests_input_files/test_file.json")

    assert parsed_file == dummy_correct_translation 


def test_pars_translation_files_wrong_file_path():
    """
    Test if pars_translation_files function handles a non-existing json file.
    """
    with pytest.raises(FileNotFoundError) as wrong_path:
        mv_avg_script.pars_translation_files("wrong_path.json")

    assert(
        str(wrong_path.value) == """File "wrong_path.json" not found. Insert an existing one."""
    )


def test_pars_translation_files_incorrect_timestamp():
    """
    Test if pars_translation_files function handles an incorrect timestamp format in the input file.
    """
    with pytest.raises(ValueError) as incorrect_timestamp:
        mv_avg_script.pars_translation_files("tests_input_files/test_file_incorrect.json")

    assert(
        str(incorrect_timestamp.value) == "Timestamp field must be in this format: Year-Month-Day Hours:Minutes:Seconds:Microseconds. \nCorrect the file."
    )


# Here start the tests for the function create_list_of_minutes
    
def test_create_list_of_minutes(dummy_correct_translation, dummy_list_of_minutes):
    """
    Test if create_list_of_minutes function works as expected, creating a list of minutes staring from the latest timestamp's minute
    and ending the most recent timestamp's minute.
    """
    list_of_minutes = mv_avg_script.create_list_of_minutes(dummy_correct_translation)

    assert list_of_minutes == dummy_list_of_minutes

def test_create_list_of_minutes_wrong_order(dummy_correct_translation):
    """
    Test if create_list_of_minutes function handles a situation when the input file is not ordered from the latest
    to the most recent timestamp.
    """
    dummy_correct_translation_reversed = dummy_correct_translation[::-1]

    with pytest.raises(Exception) as wrong_order:
        mv_avg_script.create_list_of_minutes(dummy_correct_translation_reversed)

    assert(
        str(wrong_order.value) == "File must be ordered from the latest translation to the most recent, please correct the input file."
    )


# Here start the tests to function calc_moving_average

def test_calc_moving_average(dummy_list_of_minutes, dummy_correct_translation):
    """
    Test if calc_moving_average function works as expected.
    """
    expected_output = [
        {"date": "2018-12-26 18:11:00", "average_delivery_time": 0},
        {"date": "2018-12-26 18:12:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:13:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:14:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:15:00", "average_delivery_time": 20},
        {"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5},
        {"date": "2018-12-26 18:22:00", "average_delivery_time": 31},
        {"date": "2018-12-26 18:23:00", "average_delivery_time": 31},
        {"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5},
    ]

    moving_avg = mv_avg_script.calc_moving_average(dummy_list_of_minutes, dummy_correct_translation, 10)

    assert moving_avg == expected_output

def test_calc_moving_average_wrong_window_size(dummy_correct_translation):
    """
    Test if calc_moving_average function handles a situation when the given window size is 0 or less.
    """
    with pytest.raises(Exception) as wrong_size:
        mv_avg_script.calc_moving_average(dummy_list_of_minutes, dummy_correct_translation, 0)

    assert(
        str(wrong_size.value) == "Window size value must be greater than 0."
    )

def test_calc_moving_average_different_day():
    """
    Test if calc_moving_average function works as expected when considering calculations between different days.
    """
    expected_output = [
        {"date": "2018-12-26 23:58:00", "average_delivery_time": 0},
        {"date": "2018-12-26 23:59:00", "average_delivery_time": 30},
        {"date": "2018-12-27 00:00:00", "average_delivery_time": 25},
        {"date": "2018-12-27 00:01:00", "average_delivery_time": 25},
        {"date": "2018-12-27 00:02:00", "average_delivery_time": 25},
        {"date": "2018-12-27 00:03:00", "average_delivery_time": 20},
    ]

    translations = mv_avg_script.pars_translation_files("tests_input_files/test_file_dif_day.json")
    list_of_minutes = mv_avg_script.create_list_of_minutes(translations)
    moving_avg = mv_avg_script.calc_moving_average(list_of_minutes, translations, 10)

    assert moving_avg == expected_output
