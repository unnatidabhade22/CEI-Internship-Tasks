# Shopping Dataset Analysis using Pandas

## Internship Week 1 Assignment

This project was completed as part of my first week internship assignment.
The objective of this project was to learn the basics of Python, data analysis, and data cleaning using the Pandas library.

---

## Project Objective

The main goal of this project was to:

* Load and explore a shopping dataset
* Understand dataset structure and data types
* Handle missing values
* Remove duplicate records
* Perform basic data operations
* Create new derived columns
* Visualize data using charts
* Export the cleaned dataset

---

## Dataset Used

Dataset Name: **Shopping Dataset**

The dataset contains product-related information such as:

* Product title
* Ratings
* Prices
* Discounts
* Categories
* Seller details
* Product descriptions

---

## Libraries Used

The following Python libraries were used in this project:

* Pandas
* NumPy
* Matplotlib
* Seaborn

---

## Tasks Performed

### 1. Data Loading

* Loaded the CSV dataset using Pandas.

### 2. Data Exploration

* Viewed first rows using `head()`
* Checked dataset shape
* Displayed column names
* Checked data types using `dtypes`
* Used `info()` and `describe()` for understanding the dataset

### 3. Handling Missing Values

* Identified missing values using `isnull().sum()`
* Filled missing values in the `discount` column using mean values

### 4. Data Cleaning

* Removed duplicate rows
* Converted price-related columns into numeric format

### 5. Basic Operations

* Selected important columns from the dataset
* Filtered products with ratings greater than 4

### 6. Feature Engineering

Created new columns:

* `price_difference`
* `popularity`
* `quantity`
* `total_amount`

### 7. Data Visualization

Created different charts for analysis:

* Histogram
* Bar chart
* Boxplot

### 8. Exporting Cleaned Data

* Saved the cleaned dataset as a new CSV file

---

```text
CEI-Internship-Tasks
│
└── Week-1-Shopping-Analysis
    │
    ├── data
    │   └── combined_dataset.csv
    │
    ├── notebook
    │   └── analysis.ipynb
    │
    ├── cleaned_data
    │   └── cleaned_dataset.csv
    │
    └── README.md
```


---

## Key Insights

* Most products had ratings between 3.5 and 4.5
* Some columns contained missing values which were cleaned successfully
* Product prices varied significantly across categories
* Highly rated products contributed more to the popularity metric

---

## Conclusion

This project helped me understand the basic workflow of data analysis using Python and Pandas.
I learned how to clean datasets, analyze information, create visualizations, and organize a complete data analysis project using Jupyter Notebook and GitHub.
