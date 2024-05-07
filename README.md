# Translation Delivery Time - Duration Moving Average Application

As an Unbabel Engineer, it is critical to monitor the delivery time of a translation to a client since the shorter the better. For that effect, it was proposed to build a simple command line application to compute, for every minute, the moving average of the translation delivery time for the last X minutes. It was known in advance the format of the input files and the desired format for the outputs. It was also known that the input were ordered by the `timestamp` key, from the oldest to the most recent translation.

## Input File Format

The input format is the following:

```json
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "airliberty","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb3","source_language": "en","target_language": "fr","client_name": "taxi-eats","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```

## Output File Format

The expected output format is the following:

```json
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```

## Requirements

To run the implemented scripts it is necessary to have:
* Python 3.0 or above;
* Built in packages such as <u>json</u>, <u>time</u>, <u>datetime</u>, <u>argparse</u> and <u>os</u>;
* <u>Pytest</u> package used for the unit tests of the implemented functions. 

<u>**Note**</u>: Visual Studio Code was used to implement the scripts and unit tests.

## How to run the implemented application

On your terminal and if you have this repository as root, run the following command:

`python unbabel_cli.py <INPUT_FILE_PATH> <WINDOW_SIZE>`

where:

* <INPUT_FILE_PATH> is the path to the input file and must be a string;

* <WINDOW_SIZE> is the number of minutes to be considered in the moving average. If WINDOW_SIZE = 10, then the program will compute the moving average for each minute considering the last 10 minutes.

If the chosen inputs are correct the script will generate a file named <u>output_file.json</u>, which contains the moving average for each minute.

## How to run the implemented unit tests

Firstly, if necessary, <u>pytest</u> package must be installed by running the following command:

`pip install pytest`

Then, simply run the command `pytest` in your terminal as it will look for the <u>test_unbabel_cli.py</u> script and run the implemented tests.

There were many different scenarios considered to see how the program would handle them. 

* <u>**Incorrect input file**</u>: If the input file had more keys than the ones expected or had missing keys, the program would print a warning informing the user about what is wrong and the execution ends. Also, if all file's keys were correct but the values's type were not correct, the program terminates and another warning is shown;

* <u>**Incorrect timestamp format**</u>: If the timestamps are not in the correct format, which is <u>Year-Month-Day Hours:Minutes:Seconds:Microseconds</u>, the program terminates and the user is informed;

* <u>**Incorrect file path**</u>: If the path to the input file is not correct, which means the program can't find the file, a warning is also shown to the user and the program's execution ends;

* <u>**File not ordered correctly**</u>: As said, the file must be ordered from the oldest to the most recent timestamp. If this is not true, the user will be informed by a message in the terminal and the program is terminated;

* <u>**Incorrect window size**</u>: If the user inputs a window size which is not greater than 0 and an integer, the program will not start and a warning is shown to the user;

* <u>**Ability to consider different days**</u>: The last test was implemented to confirm if the program was able to handle timestamps from different days. The program passed the test successfully.

The folder **tests_input_files** must be unzipped and it is a directory with input files for the tests.

## Optimizations

Two optimizations were considered and were both related to the fact that the data is ordered according to the timestamp, from the oldest to the most recent.

* To find the <u>minimum and the maximum timestamps</u> it was not necessary to iterate through all the data, since the minimum was from the first translation and the maximum from the last record;

* When computing the moving average for a given timestamp, <u>once a translation with a greater timestamp was found</u> it was possible to stop analysing the current timestamp and proceed to the next on since we know the timestamps would keep increasing.    
