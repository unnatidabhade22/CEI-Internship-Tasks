# Shopping Dataset Analysis using Pandas

## Internship Week 1 Assignment

This project was completed as part of my Week 1 internship assignment. The main objective of this project was to learn the fundamentals of Python programming, data exploration, data cleaning, and basic data analysis using the Pandas library.

---

## Project Objective

The goals of this project were to:

* Load and analyze a shopping dataset
* Understand dataset structure and data types
* Identify and handle missing values
* Remove duplicate records
* Perform basic data operations
* Create new derived columns for analysis
* Generate visualizations for better insights
* Export the cleaned dataset for further use

---

## Dataset Information

**Dataset Used:** Shopping Dataset

The dataset contains product-related information such as:

* Product titles
* Ratings and reviews
* Initial and final prices
* Discounts
* Product categories
* Seller details
* Product descriptions

---

## Technologies and Libraries Used

The following Python libraries were used during the project:

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

---

## Tasks Performed

### 1. Data Loading

* Imported the dataset using Pandas
* Loaded the CSV file into a DataFrame

### 2. Data Exploration

* Displayed sample rows using `head()`
* Checked dataset dimensions using `shape`
* Viewed column names
* Analyzed data types using `dtypes`
* Used `info()` and `describe()` for dataset understanding

### 3. Handling Missing Values

* Identified missing values using `isnull().sum()`
* Filled missing values in the `discount` column using mean imputation

### 4. Data Cleaning

* Removed duplicate records
* Converted price-related columns into numeric format for analysis

### 5. Basic Data Operations

* Selected important columns from the dataset
* Filtered products with ratings greater than 4

### 6. Feature Engineering

Created additional columns to improve analysis:

* `price_difference`
* `popularity`
* `quantity`
* `total_amount`

### 7. Data Visualization

Generated visualizations to understand the dataset better:

* Histogram
* Bar Chart
* Boxplot

### 8. Exporting Cleaned Dataset

* Saved the cleaned dataset as a new CSV file

---

## Project Structure

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
* Missing values were successfully handled during data cleaning
* Product prices varied significantly across categories
* Highly rated products showed higher popularity scores

---

## Conclusion

This project helped me understand the complete basic workflow of data analysis using Python and Pandas. Through this assignment, I learned how to explore datasets, clean data, create meaningful features, generate visualizations, and organize a complete project using Jupyter Notebook and GitHub.
