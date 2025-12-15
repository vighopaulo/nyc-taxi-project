# NYC Taxi Data Explorer  
A simple interactive data-exploration web app built using **Streamlit** and **Pandas**.

This project was created as part of my Python coursework to demonstrate:
- Loading a large CSV dataset  
- Cleaning and preprocessing the dataset  
- Performing exploratory data analysis with Pandas  
- Building a web interface using Streamlit  
- Filtering, grouping, and visualizing data interactively  

---

## 🚕 Dataset 

	•	Source: New York City Taxi & Limousine Commission (TLC) public data (sampled)
	•	Format: CSV
	•	Size: 800+ rows, multiple categorical and numerical fields
	•	Characteristics:
	•	Mixed data types (categorical, numeric, time-like fields)
	•	Realistic structure typical of production datasets
	•	Suitable for demonstrating data cleaning and EDA workflows

The dataset file is stored locally in the repository under the data/ directory.

---

## 🧰 Application Features  

1. Data Loading & Type Handling
	•	Loads data using Pandas
	•	Automatically inspects column data types
	•	Attempts conversion of date/time-like columns
	•	Uses caching to improve performance

2. Raw Data Inspection
	•	Displays the first 50 rows of the dataset
	•	Allows users to inspect the raw structure of the data

3. Data Summary & Statistics
	•	Displays full DataFrame metadata using df.info()
	•	Shows descriptive statistics using df.describe(include="all")
	•	Enables inspection of:
	•	column types
	•	non-null counts
	•	memory usage
	•	summary statistics for numeric and categorical columns

4. Interactive Filtering
	•	Filter rows based on:
	•	Numeric ranges (sliders)
	•	Date ranges (date pickers)
	•	Categorical values (multi-select)
	•	Displays filtered results immediately

5. Grouping & Aggregation
	•	Group data by a selected column
	•	Compute mean values for selected numeric columns
	•	Display aggregated tables and bar charts

6. Visualization
	•	Generate line charts for numeric columns
	•	Visualize trends and distributions directly in the app

⸻

Technologies Used
	•	Python 3
	•	Pandas – data manipulation and analysis
	•	NumPy – numerical support
	•	Streamlit – interactive web interface and deployment
	•	GitHub – version control and project hosting
---

## 🖥️ Running the App Locally  

git clone https://github.com/vighopaulo/nyc-taxi-project.git
cd nyc-taxi-project
pip install -r requirements.txt
streamlit run app.py


## (Live Deployment)

The application is deployed on Streamlit Community Cloud:

👉 Live App URL:
https://vighopaulo-nyc-taxi-project-app-9tpjw4.streamlit.app
