import logging
import os  # To create and manipulate file paths
from datetime import datetime

# This will create a log file name with the current timestamp in the format MM_DD_YYYY_HH_MM_SS.log
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# This creates the path where the log file will be Saved:
# - os.getcwd() gets the current working directory.
# - "logs" is the folder name where logs will be stored.
# - LOG_FILE is the log file name with the timestamp.
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

# This creates the "logs" folder (if it doesn't already exist) to store the log files.
os.makedirs(logs_path, exist_ok=True)

# LOG_FILE_PATH is the full path to where the log file will be saved, including both the directory and the file name
LOG_FILE_PATH=os.path.join(logs_path, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,  # Specifies where the logs will be stored (at the path created above)
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,  # Only INFO and above messages will be logged
)
