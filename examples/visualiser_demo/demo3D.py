from flighthouse import visualise3D
import os

# First we determine where this script is and obtain the absolute file path to the output json file.
# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    demo_file = 'real_flight.json'
    # Construct the path to the JSON file
    json_file_path = os.path.join(script_dir, demo_file)

    # Call the visualiser. Experiment with the following:
    # TODO change the history_length
    # TODO set show_sheets to True/False to show/hide the transparent sheets
    # TODO change the interval (in milliseconds) to change the time between frames
    # NOTE there will be a lower bound for the interval below which the animation won't run any faster
    # depending on your system 
    visualise3D(json_file_path, history_length=200, show_sheets=True, interval=1)
