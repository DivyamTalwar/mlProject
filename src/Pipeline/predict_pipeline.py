import sys 
import pandas as pd  
from src.exception import CustomException  
from src.utils import load_object
import os


# PredictPipeline class handles the prediction logic: loading model, preprocessing data, and making predictions
class PredictPipeline:
    def __init__(self):
        pass 

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")  # Define the path to the saved model
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')  # Path to the saved preprocessor

            print("Before Loading") 
            model = load_object(file_path=model_path) 
            preprocessor = load_object(file_path=preprocessor_path)
            print("After Loading")

            # Preprocess the input data using the loaded preprocessor (scaling the features)
            data_scaled = preprocessor.transform(features)
            
            # Make predictions using the loaded model on the scaled data
            preds = model.predict(data_scaled)
            return preds 

        except Exception as e:
            raise CustomException(e, sys)  # If an error occurs, raise a custom exception with details

# CustomData class holds the user input data and converts it into a DataFrame format
class CustomData:
    # Initialization method stores the user input data
    def __init__(self, gender: str, race_ethnicity: str, parental_level_of_education, lunch: str, 
                 test_preparation_course: str, reading_score: int, writing_score: int):
        self.gender = gender  
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch  
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score  

    # Convert the stored data into a pandas DataFrame
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys) 
