# How to obtain MET-min/week using GPAQ scores

Call the function using ```python3 gpaq.py [-d input_path] [-o output_path] [--ind]```  

`[-d]` is optional, default is ~/data/ in the same folder.  
`[-o]` is optional, default is ~/results/ in the same folder.  
`[--ind]` is optional and permits to save individual files. Default is one concatenated file.  

Exemple: ```python3 gpaq.py -d /Users/Me/Desktop/gpaq/myData/ -o /Users/Me/Desktop/gpaq/myResults/ --ind``` 

GPAQ questionnaires assess the physical activity (PA) behavior during work, displacements or hobbies.
You can then obtain the number of minutes per week spend practicing moderate (MPA), vigorous (VPA), or no PA; then translate it into MET/min/week.  
  
To do so, you need to:
* transpose your paper/pdf/online questionnaires into .csv files, and put them all in the same folder (see exemple of file structure in [~/data/](https://github.com/MatthieuGG/GPAQ-scores/tree/main/data))
* call the software provided on your transposed .csv files to obtain the energy expenditure over a week (see [~/results/](https://github.com/MatthieuGG/GPAQ-scores/tree/main/results)). You can run the code as is if you keep the same path.
* This notebook imports the data, check for conditions (duplicates, missing data, inconsistancy), and calculates the different values of PA, then saves the results.
---
We based our calculation on the [GPAQ guides](https://www.who.int/docs/default-source/ncds/ncd-surveillance/gpaq-analysis-guide.pdf) and [ONAPS recommandations](https://onaps.fr/wp-content/uploads/2020/10/Interpre%CC%81tation-GPAQ.pdf).

**To cite this work:**
> Matthieu Gallou-Guyot. (2023). GPAQ-scores. Zenodo. https://doi.org/10.5281/zenodo.10060405  

----
**Note**: did a "git remote add upstream https://github.com/MatthieuGG/GPAQ-scores" to stay up-to-date of the original repo. <br> use "git pull --rebase upstream main" to get the new commits.
