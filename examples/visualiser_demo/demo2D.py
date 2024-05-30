from flighthouse import SimulationVisualizer
import os


# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
json_file_path = os.path.join(script_dir, 'example_output.json')


if __name__ == "__main__":
    visualizer = SimulationVisualizer(json_file_path)
    visualizer.show_plot()