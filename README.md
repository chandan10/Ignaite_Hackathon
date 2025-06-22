# PowerBi-AI-App
Upload BRD docs, get a Power BI dashboard image, and download it
## Prerequisites
**Python** (Install Python 3.7.9 or higher )

## Setup
1. Clone the repository.
2. Install dependencies by running:
   
bash
pip install -r pip-requirements.txt
   

## Run App Locally
Run app locally using the following command:
streamlit run app.py

It will open in your browser at:
http://localhost:8501


## Folder Structure
powerbi-ai-app/: Main folder which contains the app code

powerbi-ai-app/
├── app.py                      # Your main Streamlit script
├── requirements.txt            # Python dependencies
└── .streamlit/
    └── secrets.toml (ignored in GitHub, used locally)

## gitignore
.gitignore file to exclude sensitive files:

.streamlit/secrets.toml
__pycache__/
*.pyc

