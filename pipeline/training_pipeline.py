from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from config.paths_config import *

if __name__ == "__main__":
    processor = DataProcessing(RAW_FILE_PATH, PROCESSED_DIR)
    processor.run()

    trainer = ModelTraining(PROCESSED_DIR, MODEL_DIR)
    trainer.run()