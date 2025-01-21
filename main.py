from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from Network_Security.entity.config_entity import TrainingPipelineConfig
from Network_Security.components.data_transformation import DataTransformation
import sys

if __name__ == '__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact = data_ingestion.initate_data_ingestion()
        logging.info("data intiate completed")
        print(dataingestionartifact)
        
        
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
        
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Initiate the data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Ending the data Transformation")
        print(data_transformation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)