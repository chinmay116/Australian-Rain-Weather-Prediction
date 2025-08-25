import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

        os.makedirs(self.output_path, exist_ok=True)
        logger.info("Data Processing Initialized!!!")

    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data Loaded Successfully!!!")
        except Exception as e:
            logger.error(f"Error Occured while Loading data {e}")
            raise CustomException("Failed to load data", e)
        
    def preprocess(self):
        try:
            categorical = []
            numerical = []

            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    categorical.append(col)
                else:
                    numerical.append(col)
            self.df["Date"] = pd.to_datetime(self.df["Date"])
            self.df["Year"] = self.df["Date"].dt.year
            self.df["Month"] = self.df["Date"].dt.month
            self.df["Day"] = self.df["Date"].dt.day

            self.df.drop("Date", axis=1, inplace=True)

            for col in numerical:
                self.df[col].fillna(self.df[col].mean(), inplace=True)

            self.df.dropna(inplace=True)

            logger.info("Basic Data Preprocessing!!!")
        except Exception as e:
            logger.error(f"Error Occured while Preprocess data {e}")
            raise CustomException("Failed to Preprocess data", e)
        
    def label_encode(self):
        try:
            categorical = [
                'Location',
                'WindGustDir',
                'WindDir9am',
                'WindDir3pm',
                'RainToday',
                'RainTomorrow']
            
            for col in categorical:
                label_encoder = LabelEncoder()
                self.df[col] = label_encoder.fit_transform(self.df[col])
                label_mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))
                logger.info(f"Label Mapping for {col}")
                logger.info(label_mapping)

            logger.info("Label Encoding Done!!!")
        except Exception as e:
            logger.error(f"Error Occured while Label Encoding {e}")
            raise CustomException("Failed to Label Encode", e)
        
    def split_data(self):
        try:
            X = self.df.drop('RainTomorrow', axis=1)
            Y = self.df['RainTomorrow']

            logger.info(X.columns)

            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            joblib.dump(X_train, os.path.join(self.output_path, "X_train.pkl"))
            joblib.dump(X_test, os.path.join(self.output_path, "X_test.pkl"))
            joblib.dump(y_train, os.path.join(self.output_path, "y_train.pkl"))
            joblib.dump(y_test, os.path.join(self.output_path, "y_test.pkl"))

            logger.info("Splitted and Saved Sucessfully!!!")
        except Exception as e:
            logger.error(f"Error Occured while Splitting data {e}")
            raise CustomException("Failed to Split data", e)
        
    def run(self):
        self.load_data()
        self.preprocess()
        self.label_encode()
        self.split_data()

        logger.info("Data Processing Completed!!!")

if __name__ == "__main__":
    processor = DataProcessing(RAW_FILE_PATH, PROCESSED_DIR)
    processor.run()