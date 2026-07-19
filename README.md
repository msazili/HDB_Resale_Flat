# HDB Resale Flat

## 1. Summary

The purpose of this project is to implement data pipeline to ingest HDB Resale Flat data from data.gov.sg and transform the data using Python.

- **Created By:** Sazili Muhammad


## 2. Features

- **ETL Pipeline** (Extract - Transform - Load)
- **Python 3** for data processing
- **Data Validation**
- **Development** environment using `uv`


## 3. Note

Please run **uv run main.py** to extract HDB Resale Flat data from data.gov.sg and store all generated data in **output** folder.


## 4. How to run

```bash
# Install dependencies
uv sync

# Run pipeline and analysis
uv run main.py
