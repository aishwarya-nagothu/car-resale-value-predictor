\# Car Resale Value Predictor



\## Overview



As educational institutions transition towards sustainable transportation, many are replacing their existing fuel-based vehicles with electric vehicles. In this project, a machine learning solution was developed to estimate the resale value of used SUV cars based on real-world market data collected from Hyderabad.



The objective is to help organizations make informed decisions when selling their used vehicles by predicting a fair market price using historical listings and vehicle characteristics.



\---



\## Problem Statement



A college plans to sell its existing fleet of SUV cars to transition towards electric vehicles. To determine a fair selling price, the institution requires a data-driven valuation system rather than relying on subjective estimates.



The goal of this project is to build a machine learning model capable of predicting the expected resale price of used SUVs by analyzing market listings from a popular used-car platform.



\---



\## Project Workflow



\### 1. Data Collection



\* Used \*\*Selenium\*\* for web scraping.

\* Collected approximately \*\*270 SUV listings\*\* from Spinny.

\* Extracted information including:



&#x20; \* Car Name

&#x20; \* Listed Price

&#x20; \* Vehicle Overview

&#x20; \* Quality Report Details



\### 2. Data Cleaning and Feature Engineering



Performed extensive preprocessing and exploratory data analysis (EDA):



\* Handled missing values

\* Removed inconsistencies and duplicates

\* Standardized categorical features

\* Extracted useful information from vehicle descriptions

\* Created additional derived features

\* Analyzed distributions, correlations, and feature importance



\### 3. Model Development



Multiple machine learning algorithms were trained and evaluated.



The workflow included:



\* Data splitting

\* Feature encoding

\* Feature scaling

\* Model training

\* Performance evaluation

\* Model comparison



The best-performing model(gradient boosting tuned) was selected based on prediction accuracy and generalization performance.



\### 4. Deployment



A user-friendly web application was developed using \*\*Streamlit\*\*.



Users can:



\* Enter vehicle details

\* Generate instant resale price predictions

\* Obtain data-driven valuation estimates



\---



\## Tech Stack



\### Data Collection



\* Python

\* Selenium



\### Data Analysis



\* Pandas

\* NumPy

\* Matplotlib

\* Seaborn



\### Machine Learning



\* Scikit-learn



\### Deployment



\* Streamlit



\---



\## Project Structure



```text

stage1\_scraping.py          # Data collection using Selenium

stage2\_cleaning.py          # Data preprocessing

stage2\_enhancing.py         # Feature engineering

stage3\_eda.ipynb            # Exploratory Data Analysis

stage4\_training.ipynb       # Model training and evaluation

stage5\_deployment.ipynb     # Deployment preparation

stage6\_streamlit\_app.py     # Streamlit application



model.pkl                   # Trained model

scaler.pkl                  # Feature scaler

feature\_names.pkl           # Feature metadata

```



\---



\## Key Features Used



\* Brand

\* Model

\* Fuel Type

\* Transmission Type

\* Manufacturing Year

\* Kilometers Driven

\* Vehicle Condition Indicators

\* Additional attributes extracted during feature engineering



\---



\## Results



The machine learning model successfully learns pricing patterns from real-world used SUV listings and provides reliable resale price estimates for vehicles in the Hyderabad market.



The solution demonstrates how web scraping, data preprocessing, machine learning, and deployment can be combined to solve a practical business problem.



\---



\## Author



Aishwarya Nagothu - B.Tech CSE | Mathathi Patak - B.Tech CSE | Charvi Parmar - B.Tech CSE| Alampuri Rohini - B.Tech CSE

