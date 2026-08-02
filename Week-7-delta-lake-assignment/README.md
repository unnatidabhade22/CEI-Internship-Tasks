# Week 7 – Delta Lake MERGE Implementation

## Objective

Learn how to perform incremental data processing using Delta Lake by creating a Delta table, cleaning data, generating incremental records, applying the MERGE operation, and validating the final results.

---

## Topics Covered

- Delta Lake Fundamentals
- Delta Table Creation
- Data Cleaning
- Removing Duplicates
- Handling Null Values
- Incremental Data Processing
- MERGE Operation
- Update Existing Records
- Insert New Records
- Data Validation
- Spark DataFrames

---

## Tools Used

- Python
- Apache Spark (PySpark)
- Delta Lake
- Google Colab

---

## Dataset

Sample - Superstore Dataset

---

## Folder Structure

```text
Week-7-delta-lake-assignment/
│
├── data/
│   ├── Sample - Superstore.csv
│   └── superstore_incremental.csv
│
├── notebooks/
│   └── delta_lake_merge_implementation.ipynb
│
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── scd1/
│   ├── scd2/
│   └── validation/
│
└── README.md
```

---

## Assignment Workflow

1. Loaded the Superstore dataset into a Spark DataFrame.
2. Created a Delta table from the dataset.
3. Performed data cleaning by removing duplicates and handling null values.
4. Generated an incremental dataset containing updated and new records.
5. Applied the Delta Lake MERGE operation.
6. Updated existing records and inserted new records.
7. Validated the final dataset by checking row count and duplicate records.
8. Displayed the final Delta table.

---

## Outcome

Successfully implemented Delta Lake MERGE for incremental data processing using Apache Spark. The assignment demonstrated how Delta Lake efficiently updates existing records, inserts new records, and maintains data consistency while supporting scalable data engineering workflows.
