# AI-Powered Data Cleaning Agent 🤖📊

An interactive, AI-ready data profiling and cleaning tool built with Python and Streamlit. This application allows users to upload raw datasets (CSV/Excel), instantly scans for anomalies like missing values and hidden text in numeric columns, and pinpoints exactly where errors occur down to the row index. 

It is designed to rapidly prepare raw, messy datasets for clean insertion into SQL databases or for training predictive machine learning models (such as XGBoost or TensorFlow).

## ✨ Features

* **Instant Data Profiling:** Upload any `.csv` or `.xlsx` file and instantly view a data preview.
* **Exact Row & Column Tracking:** Doesn't just give you aggregate counts. It isolates the exact row indices where `NaN` values or type mismatches exist, allowing for targeted auditing.
* **Smart Type Mismatch Detection:** Uses Pandas coercion logic to sniff out hidden alphabetical characters or symbols inside columns that should be strictly numeric.
* **Automated Cleaning Pipeline:** Opt to clean the data with one click. Automatically coerces rogue text to `NaN`, fills missing numeric values with the column median, and fills missing text with "Unknown".
* **One-Click Export:** Download the fully cleaned dataset immediately as a new CSV.

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit** (Frontend UI)
* **Pandas** (Data manipulation and cleaning logic)
* **Google GenAI API** (Framework ready for LLM-driven semantic cleaning and context-aware imputation)
