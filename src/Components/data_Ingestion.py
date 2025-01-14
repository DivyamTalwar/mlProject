import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass # Dataclass decorator to simplify class creation for data storage


#This class DataIngestionConfig defines the paths for storing the data.These paths are inside the "artifacts" directory
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")   # This will create a path where training data will be stored
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

#This class is responsible for ingesting (loading) data into the system
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() #when you call this class the 3 paths defined above will be saved in this var

    def initiate_data_ingestion(self):
        # Log the start of the data ingestion process
        logging.info("Entered the data ingestion method or component")
        
        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            # This ensures that the dir where the train data will be store already exist if yes continue if no make the directary
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save the entire dataset (raw) to the specified path
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the training set to the specified file path
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            # Save the test set to the specified file path
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            # Return the paths to the train and test datasets
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)

# Main function to execute the script when run directly
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

