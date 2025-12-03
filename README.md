# **Course Schedule Optimization Project**

## Project Files

I have four python files as part of my program to generate all possible class schedule options at a university given the possible class times.

### (1) SchCombos.py
Takes in one list of lists of dictionaries and prints a list of a possible schedule combinations to valid_schedules.txt

### (2) converter.py
Inputs a multi-line string of one possible schedule combination and outputs it in a format that can be taken in by visualizer.py

### (3) visualizer.py
Takes the output of converter.py and uses the matplotlib.pyplot library to provide a plot of the schedule

### (4) text_based_app.py
Uses the methods in the previous three .py files to run the program

## Streamlit

TO RUN, USE streamlit run streamlit_app.py
