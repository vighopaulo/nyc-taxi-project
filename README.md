# NYC Taxi Data Explorer  
Project Overview

This project presents an exploratory data analysis (EDA) of a large New York City taxi dataset using Python and the pandas library. The objective is to demonstrate practical data handling skills, including data cleaning, inspection, transformation, aggregation, and visualization. An optional interactive interface is provided to support exploratory analysis, but the primary emphasis of the project is on data preparation and analytical logic, not application deployment.

## 🚕 Dataset Description

The dataset contains monthly operational statistics for different NYC taxi and for-hire vehicle (FHV) license classes. Key variables include:
	•	Month/Year
	•	License Class
	•	Trips Per Day
	•	Farebox Per Day
	•	Unique Drivers
	•	Unique Vehicles
	•	Vehicle utilization and trip-duration metrics

The dataset includes a mix of numeric, categorical, and date-like fields, as well as missing values and numeric values stored as text.
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
## Data Cleaning and Preparation

Several data cleaning steps were applied programmatically to prepare the dataset for analysis:
	1.	Column name standardization
	•	Whitespace was stripped from column names to ensure consistency.
	2.	Date handling
	•	Columns with date- or time-related names were automatically detected and converted to datetime format where possible.
	3.	Numeric conversion
	•	Numeric values stored as text (e.g., "647,819") were cleaned by removing thousands separators.
	•	Placeholder symbols such as "-" were treated as missing values.
	•	Cleaned values were converted to numeric types where applicable.
	4.	Missing value handling
	•	Missing values were preserved as NaN to allow pandas to handle them correctly during aggregation and statistical analysis.
	5.	Dynamic data typing
	•	Columns were programmatically classified as numeric, categorical, or datetime to support flexible analysis without hard-coded assumptions.
	
## Exploratory Analysis Performed

The project demonstrates a range of exploratory data analysis operations, including:
	•	Inspection of raw data samples
	•	Dataset structure and summary statistics (DataFrame.info() and describe)
	•	Conditional row filtering for numeric, categorical, and datetime fields
	•	Grouping and aggregation (mean values by category)
	•	Trend visualization of numeric variables
	•	Category-based comparisons (e.g., average trips by license class)
	•	Distribution analysis using binned frequency counts

All analytical operations are implemented using pandas and are reproducible from the source code.

## Technologies Used

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

## Repository Structure
nyc-taxi-project/
│
├── app.py              # Data loading, cleaning, and exploratory analysis logic
├── data/
│   └── sample_data.csv # Dataset used for analysis
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore

## (Live Deployment)

The application is deployed on Streamlit Community Cloud:

👉 Live App URL:
https://vighopaulo-nyc-taxi-project-app-9tpjw4.streamlit.app
