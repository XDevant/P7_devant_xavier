These scrips calculate the best possible income for a 500$ portfolio of shares.

The spimplest way to test it is to:
1. Clone the repository on your own computer.

2. Create a new virtual environment in the same folder as scrap.py:

        python -m venv env

3. Activate the virtual environment
    + unix: source env/bin/activate
    + windows: env/Scripts/activate.bat

4. Install the dependencies via the requirement.txt file

        pip install -r requirements.txt

5. Run bruteforce.py (only runs on dataset0):

        python tournamentmanager.py

6. Run brute-optimized or optimized.py followed by the csv file name:

        python optimized.py dataset1_Python+P7.csv


