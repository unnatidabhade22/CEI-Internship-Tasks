# Week 4 - Azure Cloud Fundamentals & Azure Data Factory

## Overview

This week's assignment focused on understanding Microsoft Azure cloud services and building an end-to-end data pipeline using Azure Storage and Azure Data Factory (ADF).

The objective was to gain practical experience with cloud resources, data movement, metadata validation, pipeline execution, and Azure access management.

---

## Assignment Tasks

### Task 1 – Azure Resource Setup
- Explored the Azure Portal.
- Created a Resource Group for organizing cloud resources.

### Task 2 – Storage Configuration
- Created an Azure Storage Account.
- Created Blob Storage containers.
- Uploaded the Superstore CSV dataset.

### Task 3 – Azure Data Factory Basics
- Created an Azure Data Factory instance.
- Explored Author, Monitor, and Manage modules.
- Configured Linked Service.
- Created Source and Destination datasets.
- Used the Get Metadata activity to validate the source file.

### Task 4 – Pipeline Development
- Built a data pipeline using the Copy Data activity.
- Configured source and destination datasets.
- Designed the complete pipeline workflow.

### Task 5 – Pipeline Execution
- Executed the pipeline using Debug.
- Successfully monitored the pipeline execution.

### Task 6 – IAM Configuration
- Assigned Reader and Contributor roles.
- Configured required access permissions between Azure Data Factory and Azure Storage.

---

# Mini Project

## Problem Statement

Build an end-to-end Azure Data Factory pipeline that reads a CSV file from Azure Blob Storage, validates its metadata, and copies it to a destination container.

## Solution

The pipeline performs the following sequence:

1. Reads the CSV file from Azure Blob Storage.
2. Retrieves file metadata using the Get Metadata activity.
3. Copies the dataset to a destination Blob container.
4. Successfully completes the pipeline execution.
5. Verifies that the copied file is available in the destination container.

---

## Technologies Used

- Microsoft Azure
- Azure Resource Group
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory (ADF)
- Linked Services
- Datasets
- Get Metadata Activity
- Copy Data Activity

---

## Dataset

Superstore Sales Dataset

---

## Repository Contents

- Assignment_Results.pdf
- Mini_Project.pdf
- README.md

---

## Learning Outcomes

- Azure cloud fundamentals
- Resource Group management
- Storage Account configuration
- Blob Storage operations
- Azure Data Factory basics
- Linked Services
- Dataset creation
- Metadata validation
- Data pipeline development
- Pipeline execution and monitoring
- Azure IAM role assignment

