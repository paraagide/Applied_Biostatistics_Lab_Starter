# Applied Biostatistics Lab

**Course:** Applied Biostatistics and Data Analytics for Pharmaceutical Sciences

A Streamlit teaching laboratory for biostatistical concepts and pharmaceutical data analytics.

## Project structure

```text
Applied_Biostatistics_Lab/
├── Home.py
├── pages/
│   ├── 01_Descriptive_Statistics.py
│   ├── 02_Probability_Distributions.py
│   ├── 03_Sampling_Inference.py
│   ├── 04_Correlation_Regression.py
│   └── 05_Case_Based_Analysis.py
├── data/
├── utils/
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally on Windows

1. Install Python 3.11 or 3.12 and VS Code.
2. Open this folder in VS Code, then select **Terminal → New Terminal**.
3. Create a virtual environment:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Run the app:

   ```powershell
   python -m streamlit run Home.py
   ```

The local app usually opens at `http://localhost:8501`.

## Publish for students

Create a **new, separate GitHub repository**, commit and push this folder using GitHub Desktop, then create a new app in Streamlit Community Cloud. Select the new repository and branch, and set the main file path to `Home.py`.

Do not overwrite the existing project or upload identifiable patient data, confidential college records, passwords, or API keys.

## Development approach

Build and test one unit at a time. Keep each unit in its own file under `pages/`, and put reusable functions in `utils/`.
