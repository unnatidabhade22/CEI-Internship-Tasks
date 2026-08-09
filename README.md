# E-Commerce Data Engineering Pipeline
***Note 1: For the assignments completed during my 2-month internship at Celebal Technologies, please refer to the main branch of the same repository.***<br>
***(Note 2: For the outputs, please refer to the `Screenshots` folder and for the project report, please refer to the `Documentation` folder.)***<br>
An end-to-end E-Commerce Data Engineering project that transforms raw customer, inventory, order, and order-item data into validated, business-ready datasets and an executive Power BI dashboard.

The project follows a layered data architecture using Python, PySpark, Delta Lake, Azure Data Lake Storage Gen2, Azure Databricks, Azure Data Factory, and Power BI.

---

## Project Overview

The pipeline processes four source datasets:

* `customers.csv`
* `inventory.csv`
* `orders.csv`
* `order_items.csv`

The data moves through multiple processing layers where it is ingested, cleaned, validated, transformed, and prepared for business analysis.

### Overall Architecture

```text
Source Data
    |
    v
Landing
    |
    v
Bronze
    |
    v
Silver
    |
    v
Data Quality Validation
    |
    +------> Quarantine
    |
    v
Delta / SCD Type-1
    |
    v
Gold
    |
    v
Reconciliation
    |
    v
Power BI Dashboard
```

---

## Azure Architecture

```text
Azure Data Lake Storage Gen2
            |
            v
    Azure Data Factory
            |
            v
     Azure Databricks
            |
            v
      Bronze / Silver
            |
            v
   Data Quality / Quarantine
            |
            v
     Delta / SCD Type-1
            |
            v
          Gold
            |
            v
    Reconciliation
            |
            v
    Power BI Dashboard
```

---

## Technology Stack

| Technology                   | Purpose                                         |
| ---------------------------- | ----------------------------------------------- |
| Python                       | Pipeline development and data processing        |
| Pandas                       | Source data inspection and profiling            |
| PySpark                      | Data transformation and processing              |
| Apache Spark                 | Distributed data processing engine              |
| Delta Lake                   | Transactional storage and SCD Type-1 processing |
| Azure Data Lake Storage Gen2 | Cloud data storage                              |
| Azure Databricks             | Cloud-based Spark processing                    |
| Azure Data Factory           | Pipeline orchestration and scheduling           |
| Power BI                     | Business reporting and visualization            |
| GitHub                       | Source control and project documentation        |

---

## Source Data

The project uses four main datasets.

| Dataset           | Records | Description                       |
| ----------------- | ------: | --------------------------------- |
| `customers.csv`   |  10,000 | Customer information              |
| `inventory.csv`   |   5,000 | Product and inventory information |
| `orders.csv`      |  50,150 | Customer order information        |
| `order_items.csv` | 200,000 | Product-level order transactions  |

Initial profiling was performed to identify:

* Missing values
* Duplicate records
* Data types
* Invalid values
* Data quality issues
* Referential integrity issues

---

# Data Pipeline

## 1. Landing Layer

The Landing layer preserves incoming source files before transformation.

```text
landing/
├── customers/
├── inventory/
├── orders/
└── order_items/
```

The ingestion process:

* Checks source files
* Creates required directories
* Copies the source files
* Records ingestion information
* Preserves the original source data

This layer provides a reliable starting point for the pipeline.

---

## 2. Bronze Layer

The Bronze layer preserves the incoming data while adding processing metadata.

### Metadata

* `bronze_ingestion_timestamp`
* `source_file_name`
* `load_date`

```text
bronze/
├── customers/
├── inventory/
├── orders/
└── order_items/
```

The Bronze layer maintains the raw structure of the data while making it traceable through metadata.

---

## 3. Silver Layer

The Silver layer contains cleaned and standardized data.

### Processing

The following transformations are performed:

* Duplicate removal
* Data type conversion
* Date and timestamp conversion
* Missing value handling
* Text standardization
* Email standardization
* Numeric validation
* Business-rule validation

```text
silver/
├── customers/
├── inventory/
├── orders/
└── order_items/
```

The Silver layer provides cleaner and more reliable data for validation and downstream processing.

---

## 4. Data Quality and Quarantine

Data quality rules are applied before downstream analytics.

### Validation Rules

The pipeline checks for:

* Missing identifiers
* Invalid dates
* Invalid quantities
* Invalid prices
* Invalid order amounts
* Missing line totals
* Invalid inventory quantities
* Referential integrity issues

Records that fail validation are separated into the Quarantine layer with a `quarantine_reason` field.

```text
quarantine/
├── customers/
├── inventory/
├── orders/
└── order_items/
```

### Data Quality Flow

```text
Silver Data
     |
     v
Data Quality Rules
     |
 +---+---+
 |       |
 v       v
Valid   Invalid
Data    Data
 |       |
 v       v
Delta  Quarantine
```

---

## 5. Referential Integrity

Relationships between the main datasets are validated to ensure that downstream joins use valid keys.

### Customer Relationship

```text
orders.customer_id
        |
        v
customers.customer_id
```

### Order Relationship

```text
order_items.order_id
        |
        v
orders.order_id
```

### Inventory Relationship

```text
order_items.sku_id
        |
        v
inventory.sku_id
```

These checks help prevent invalid joins and inconsistent analytical results.

---

# Delta Lake and SCD Type-1

Delta Lake is used for transactional processing and incremental customer updates.

Customer data arrives as periodic snapshots, so SCD Type-1 processing is applied.

### SCD Type-1 Flow

```text
Customer Snapshot
       |
       v
Compare customer_id
       |
   +---+---+
   |       |
Existing   New
   |       |
   v       v
UPDATE   INSERT
```

### Processing Logic

* If the `customer_id` already exists, the existing record is updated with the latest information.
* If the `customer_id` does not exist, a new record is inserted.
* Historical versions are not maintained.
* The latest customer information is available for downstream analytics.

This maintains the current state of customer information.

---

# Gold Layer

The Gold layer contains business-ready analytical datasets designed for reporting and decision-making.

```text
gold/
├── daily_revenue.csv
├── fulfillment_kpi.csv
├── inventory_health.csv
├── customer_ltv.csv
├── reconciliation_row_counts.csv
└── reconciliation_dq_summary.csv
```

---

## Daily Revenue

`daily_revenue.csv` provides revenue analysis by date, region, and category.

### Key Metrics

* Total Revenue
* Order Count
* Average Order Value (AOV)

---

## Fulfillment KPI

`fulfillment_kpi.csv` provides fulfillment performance by date, warehouse, and region.

### Key Metrics

* Total Orders
* Delivered Orders
* Cancelled Orders
* Shipped Orders
* Delivery Rate
* Cancellation Rate
* Shipment Rate

---

## Inventory Health

`inventory_health.csv` provides inventory and replenishment analysis.

### Key Metrics

* Total SKUs
* Stock Quantity
* Inventory Value
* Stockout Count
* Below-Reorder Count
* Overstock Count
* Reorder Requirements
* Demand

---

## Customer LTV

`customer_ltv.csv` provides customer-level value and segmentation.

### Key Metrics

* Lifetime Spend
* Order Frequency
* Recency
* Customer Segment
* Average LTV

### Customer Segments

| Segment    | Description                               |
| ---------- | ----------------------------------------- |
| VIP        | Highest-value customers                   |
| High Value | Customers with high spending and activity |
| Mid Value  | Customers with moderate value             |
| Low Value  | Customers with relatively low spending    |

---

# Reconciliation and Audit

Two reconciliation datasets are generated:

```text
reconciliation_row_counts.csv
reconciliation_dq_summary.csv
```

They provide visibility into:

* Records processed across layers
* Valid records
* Quarantined records
* Pass rates
* Quarantine rates
* Data quality results

### Reconciliation Flow

```text
Source
  |
  v
Landing
  |
  v
Bronze
  |
  v
Silver
  |
  v
Data Quality
  |
  +----> Valid Records
  |
  +----> Quarantined Records
  |
  v
Gold
  |
  v
Reconciliation
```

This provides an audit view of the pipeline and supports data quality verification.

---

# Azure Implementation

The project was extended to Azure Data Lake Storage Gen2 using a dedicated `ecommerce-data` container.

```text
ecommerce-data/
├── landing/
├── bronze/
├── silver/
├── quarantine/
└── gold/
```

---

## Azure Databricks

Azure Databricks is used as the Spark processing environment for the cloud pipeline.

The Databricks workflow processes the following stages:

```text
Landing
   |
   v
Bronze
   |
   v
Silver
   |
   v
Data Quality
   |
   v
Quarantine
   |
   v
Delta / SCD Type-1
   |
   v
Gold
   |
   v
Reconciliation
```

---

# Secure Authentication

Storage credentials are managed through a Databricks Secret Scope instead of being hardcoded into the processing logic.

```text
Scope: azure-storage
Key:   storage-account-key
```

Credentials are retrieved securely at runtime.

This improves the security of the cloud data pipeline and prevents sensitive credentials from being exposed in source code.

---

# Azure Data Factory

Azure Data Factory provides pipeline orchestration between Azure Data Lake Storage Gen2 and Azure Databricks.

The pipeline is scheduled to execute periodically and automate the processing workflow.

```text
Azure Data Factory
        |
        v
Azure Databricks
        |
        v
Data Processing Pipeline
        |
        v
Gold Data
```

---

# Power BI Dashboard

A Power BI Executive Overview dashboard was created using the Gold-layer datasets.

The dashboard provides an executive-level view of:

* Sales
* Revenue
* Customers
* Fulfillment
* Inventory

## KPI Cards

The dashboard includes:

* Total Revenue
* Total Orders
* Total Customers
* Average Customer LTV
* Delivery Rate
* Inventory Value

## Visualizations

The dashboard includes:

* Revenue by Region
* Revenue by Category

The dashboard allows business users to understand sales, customer, fulfillment, and inventory performance without directly inspecting the underlying datasets.

---

# Key Project Outcomes

This project demonstrates practical experience with:

* End-to-end Data Engineering
* Layered Data Architecture
* Data Ingestion
* Data Profiling
* Data Cleansing
* Data Validation
* Data Quarantine
* Referential Integrity
* Data Lineage
* PySpark Processing
* Apache Spark
* Delta Lake
* SCD Type-1
* Azure Data Lake Storage Gen2
* Azure Databricks
* Azure Data Factory
* Pipeline Orchestration
* Data Reconciliation
* Data Quality Auditing
* Gold-Layer Analytics
* Power BI Reporting

---

# Repository Structure

```text
Ecommerce-Data-Engineering-Project/
│
├── data/
│   ├── source/
│   ├── landing/
│   ├── bronze/
│   ├── silver/
│   ├── quarantine/
│   ├── delta/
│   └── gold/
│
├── scripts/
│   ├── config.py
│   ├── ingest_to_landing.py
│   ├── create_bronze.py
│   ├── create_silver.py
│   ├── data_quality_validation.py
│   ├── referential_integrity.py
│   ├── create_delta_customers.py
│   ├── create_gold_daily_revenue.py
│   ├── create_gold_fulfillment_kpi.py
│   ├── create_gold_inventory_health.py
│   ├── create_gold_customer_ltv.py
│   └── create_reconciliation.py
│
├── notebooks/
│
├── dashboard/
│
├── screenshots/
│
├── documentation/
│
├── README.md
│
└── .gitignore
```

---

# Final Data Flow

```text
Raw CSV Files
     |
     v
Landing
     |
     v
Bronze
     |
     v
Silver
     |
     v
Data Quality
     |
     +------> Quarantine
     |
     v
Delta / SCD Type-1
     |
     v
Gold Analytics
     |
     v
Reconciliation
     |
     v
Power BI Dashboard
```

---

# Project Summary

The completed solution demonstrates how raw E-Commerce data can be transformed into trusted, structured, cloud-based analytical data through a complete data engineering pipeline.

The project combines data ingestion, cleansing, validation, quarantine, referential integrity, Delta Lake, SCD Type-1, cloud processing, orchestration, reconciliation, and business intelligence into a single end-to-end solution.

---

# Author

**Unnati Dabhade**

**Internship:** Celebal Technologies

**Project:** E-Commerce Data Engineering Pipeline

---

# Connect With Me

* **LinkedIn:** [LinkedIn Profile](www.linkedin.com/in/unnati-dabhade-66905728b)
* **GitHub:** [GitHub Profile](https://github.com/unnatidabhade22)
* **HackerRank:** [HackerRank Profile](https://www.hackerrank.com/profile/unnatidabhade011)


---

# Acknowledgement

This project was completed as part of the internship program at **Celebal Technologies**.

The internship provided practical experience in Data Engineering, cloud data platforms, Spark processing, Azure services, Delta Lake, data quality, pipeline orchestration, and Business Intelligence.
