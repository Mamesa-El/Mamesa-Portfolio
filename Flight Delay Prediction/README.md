# United Airlines Flight Delay Prediction

## Project Overview
This project aims to predict flight delays for United Airlines using machine learning. According to the Bureau of Transportation Statistics (BTS), approximately **22.09% of United flights experienced delays in 2023**. Our goal is to build a predictive model that enables proactive measures to minimize these delays.

## Team Members
- Mamesa El (mamesa.el@berkeley.edu)
- Sam Gupta (sambhav.gupta@berkeley.edu)
- Sneha Narain (sn3ae@berkeley.edu)
- Jonathan Tran (bk_pbjonmt@berkeley.edu)

## Data Description
The project utilizes datasets derived from:
- Flight information from the US Department of Transportation (2015-2021)
- Weather data from the National Oceanic and Atmospheric Administration (2015-2021)
- Station data from the US Department of Transportation

## Machine Learning Pipeline
1. **Data Ingestion**: Loading and initial preparation of data
2. **Data Processing**: Cleaning, feature engineering, and transformation
3. **Modeling**: Implementation of machine learning algorithms
4. **Evaluation**: Assessment of model performance

## Key Features Engineered
- Weather metrics (temperature, wind speed, visibility, etc.)
- Flight details (time categories, previous flight delays, etc.)
- Airport and route-specific statistics

## Models Implemented
1. **Logistic Regression**: Baseline model
2. **Random Forest**: Enhanced decision tree-based model
3. **XGBoost**: Top-performing gradient-boosted model
4. **Multilayer Perceptron**: Neural network approach

## Results
- XGBoost demonstrated the best performance with an F1 score of **78.3%** on the validation set and **77.2%** on the held-out test set
- Successfully identified patterns in flight delays based on weather conditions, airline characteristics, and temporal factors

## Challenges Addressed
- Data leakage prevention with time series cross-validation
- Performance optimization with parquet files and MLFlow
- Scalability through Databricks implementation
- Class imbalance handling through hyperparameter tuning

## Future Work
- Improved weather dataset integration
- Advanced graph-based features for airport connectivity
- Enhanced experiment iterations and hyperparameter tuning

## Technologies Used
- PySpark for distributed data processing
- MLFlow for experiment tracking and model management
- Databricks for scalable computation
- Parquet for efficient data storage