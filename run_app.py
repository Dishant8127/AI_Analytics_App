# run_app.py
import subprocess
import os

def run():
    """
    Finds the path to the streamlit app and runs it.
    """
    # Get the directory where this script is located
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Construct the full path to the streamlit app script
    app_path = os.path.join(dir_path, 'app.py')
    
    # Command to run
    command = ["streamlit", "run", app_path]
    
    # Run the command
    subprocess.run(command)

if __name__ == '__main__':
    run()