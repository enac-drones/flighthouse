from flighthouse import SimulationVisualizer
import os

# First we determine where this script is and obtain the absolute file path to the output json file.
# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
json_file_path = os.path.join(script_dir, 'parallel_flight.json')


if __name__ == "__main__":
    visualizer = SimulationVisualizer(json_file_path)
    visualizer.show_plot()