==============================
Back-end-PM Project - Setup Guide
==============================

1) Clone the repository
------------------------
git clone https://github.com/maii-zain/Back-end-PM.git
cd Back-end-PM

2) Create a virtual environment
-------------------------------
- Windows:
    python -m venv venv

- Linux / macOS:
    python3 -m venv venv

3) Activate the virtual environment
-----------------------------------
- Windows (PowerShell):
    venv\Scripts\activate

- Linux / macOS:
    source venv/bin/activate

4) Install dependencies
------------------------
pip install -r requirements.txt

5) Download the model file
---------------------------
The model file is not included in the repository because of size limits.

- Download it from the public Google Drive link:
  https://drive.google.com/drive/u/0/folders/1Qpr4pNgK11VXIwZ5JZ0M5ctDANu7k2vI

- After download, place the model file into a folder called:
  model_files/

- The folder structure should look like this:
  Back-end-PM/
  ├── model_files/
  │   └── your_model_file.pkl
  ├── manage.py
  ├── requirements.txt
  └── ...

6) Apply Django migrations
---------------------------
python manage.py migrate

7) Run the development server
-----------------------------
python manage.py runserver


==============================
Notes
==============================
- Always activate the virtual environment before running commands.
- If new packages are added, update the requirements file:
  pip freeze > requirements.txt
- The model must be placed in "model_files/" to enable predictions.
