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
The project uses NYC Taxi & Limousine Commission public dataset samples.

The sample file included here is a small CSV used for demonstration.  
You can replace this file with **any** CSV as long as you update the column names in the app if needed.

---

## 🧰 Features  

### ✔ Data Loading & Cleaning  
- Automatic detection of numeric, datetime, and text columns  
- Invalid values removed  
- Trip duration and trip rate feature-engineering  

### ✔ Interactive Tools  
The Streamlit sidebar allows you to perform:

#### **1. View Raw Data**  
Displays the first 50 rows.

#### **2. Describe Data**  
Shows Pandas `.describe()` summary statistics.

#### **3. Filter Rows**  
Supports:
- Numeric range filters  
- Date/time filters  
- Text/category filters  

#### **4. Group & Aggregate**  
Group by any column and compute mean values.

#### **5. Plot Numeric Columns**  
Generate line charts for numeric columns.

---

## 🖥️ Running the App Locally  

### **1. Clone the repository**
```bash
git clone https://github.com/vighopaulo/nyc-taxi-project.git
cd nyc-taxi-project
