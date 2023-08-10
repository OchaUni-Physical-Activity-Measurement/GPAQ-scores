# How to obtain MET/min/week using GPAQ scores ?
GPAQ questionnaires assess the physical activity (PA) behavior during work, displacements or hobbies.
You can then obtain the number of minutes per week spend practicing moderate (MVPA), intense (VPA), or no physical activity; then translate it into MET/min/week.  
  
To do so, you need to:
* transpose the questionnaires into .csv files (see model provided)
* put all the .csv files in the same folder
* use the code provided (**Scoring GPAQ.ipynb**) on your transposed .csv files to obtain the energy expenditure over a week. You have to precise the path of the folder where all the .csv are, and the path where you want to save the result

# How to obtain MET/min/week using Fitbit data as GPAQ scores ?
Fitbit PA trackers can provide you steps, kcal, MET and intensity of PA per minute. Based on the GPAQ calculation, you can obtain the number of minutes per week spend practicing moderate (MVPA), intense (VPA), or no physical activity; then translate it into MET/min/week.  
  
To do so, you need to:
* get all the .csv files with per-minute PA data
* put all the .csv files in the same folder
* use the code provided (**Scoring Fitbit as GPAQ.ipynb**)on your transposed .csv files to obtain the energy expenditure over a week. You have to precise the path of the folder where all the .csv are, and the path where you want to save the result
