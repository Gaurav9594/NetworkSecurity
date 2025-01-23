import sys
import os
from Network_Security.exception.exception import NetworkSecurityException
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from Network_Security.constants.training_pipeline import TARGET_COLUMN
from Network_Security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from Network_Security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from Network_Security.entity.config_entity import DataTransformationConfig
from Network_Security.logging.logger import logging
from Network_Security.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact= data_validation_artifact
            self.data_transformation_config :DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initiates a KNNImputer object with the parameter specified in the training_pipeline.py file
        and return a Pipeline object with the KNNImputer object as the first step
        
        Args : DataTransformation
        
        Return : A pipeline object
        """
        try:
            logging.info("Enter get_data_transformer_object method of Transformation class")
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            # ** : This means that the params will be consideered as key value pair
            
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Starting data transformation")
        try:
            logging.info("Starting data transformation")
            # reading train and test df
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## training dataframe
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN], axis = 1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            
            ## testing dataframe
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN], axis = 1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)
            
            # transformation of the data using pipeline
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transform_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transform_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            # Both above variable will be an array
            
            train_arr = np.c_[transform_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transform_input_test_feature, np.array(target_feature_test_df)]
            # .c_ : combines both the params in the function
            
            # savw numoy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr, )
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr, )
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object, )
            
            # preparing Arrtifacts
            # this will be returned once we completeed out data transformation
            data_transforamtion_artifact = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )
            return data_transforamtion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    