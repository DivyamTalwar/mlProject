import sys
from dataclasses import dataclass
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler , OrdinalEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

#@dataclass simplifies class creation by auto-generating methods like __init__
@dataclass
class DataTransformationConfig:
    #this is create a file inside aftifacts for preprocessing the data
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function defines the data transformation pipeline for preprocessing data.
        It includes handling missing values, scaling numerical data, and applying different encoding techniques.
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns_ohe = ["race_ethnicity", "lunch", "test_preparation_course"]
            categorical_columns_oe = ["parental_level_of_education", "gender"]

            # Defining the order for Ordinal Encoding
            education_order = [
                "some high school", 
                "high school", 
                "some college", 
                "associate's degree", 
                "bachelor's degree", 
                "master's degree"
            ]

            gender_order = ["female", "male"]

            ordinal_categories = [education_order, gender_order]

            # Pipeline for numerical data
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # Pipeline for categorical data where OHE will be applied
            cat_ohe_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(drop='first')),  # Applying OneHotEncoder
                    ("scaler", StandardScaler(with_mean=False))  # Scaling after encoding
                ]
            )

            # Pipeline for categorical data where OE will be applied
            cat_oe_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("ordinal_encoder", OrdinalEncoder(categories=ordinal_categories)),  # Applying OrdinalEncoder with order
                    ("scaler", StandardScaler(with_mean=False))  # Scaling after encoding
                ]
            )

            logging.info(f"Categorical columns (OHE): {categorical_columns_ohe}")
            logging.info(f"Categorical columns (OE): {categorical_columns_oe}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combining all transformations using ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),  # Numerical pipeline
                    ("cat_ohe_pipeline", cat_ohe_pipeline, categorical_columns_ohe),  # OHE pipeline
                    ("cat_oe_pipeline", cat_oe_pipeline, categorical_columns_oe)   # OE pipeline with defined order
                ]
            )

            return preprocessor  # Return the preprocessor object for use in transformation

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"  # Output or Dependent Feature
            
            # Splitting the training and test data into input features and target columns
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes.")

            # Applying the preprocessing transformations on the input data (fit_transform on train, transform on test)
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combining the transformed input features and target values into arrays for training & test the model
            #we use np.c_ to concatenate array about the column (axis = 1)
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]  # Training data
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  # Testing data

            logging.info("Saved preprocessing object.")

            # Saving the preprocessing object(one defied above) to a file for future use (reuse the same transformation)
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path, obj=preprocessing_obj)

            # Returning the transformed data and the path to the saved preprocessing object
            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path
        
        except Exception as e:
            raise CustomException(e, sys)
