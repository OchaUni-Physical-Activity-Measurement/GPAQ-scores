# How to obtain MET-min/week using GPAQ scores

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10086826.svg)](https://doi.org/10.5281/zenodo.10086826)

**Input: individual .csv files (["~/sample"](https://github.com/MatthieuGG/GPAQ-scores/tree/main/sample))**  
**Output: individual and comon .csv files (["~/results"](https://github.com/MatthieuGG/GPAQ-scores/tree/main/results))**  
**Script: [Scoring GPAQ.ipynb](https://github.com/MatthieuGG/GPAQ-scores/blob/main/Scoring%20GPAQ.ipynb)**  


GPAQ questionnaires assess the physical activity (PA) behavior during work, displacements or hobbies.
You can then obtain the number of minutes per week spend practicing moderate (MPA), vigorous (VPA), or no PA; then translate it into MET/min/week.  
  
To do so, you need to:
* transpose your paper/pdf/online questionnaires into .csv files, and put them all in the same folder (see exemple of file structure in ["~/sample"](https://github.com/MatthieuGG/GPAQ-scores/tree/main/sample))
* use the code provided (**[Scoring GPAQ.ipynb](https://github.com/MatthieuGG/GPAQ-scores/blob/main/Scoring%20GPAQ.ipynb)**) on your transposed .csv files to obtain the energy expenditure over a week (see ["~/results"](https://github.com/MatthieuGG/GPAQ-scores/tree/main/results)). You can run the code as is if you keep the same path. 

We based our calculation on the [GPAQ guides](https://www.who.int/docs/default-source/ncds/ncd-surveillance/gpaq-analysis-guide.pdf) and [ONAPS recommandations](https://onaps.fr/wp-content/uploads/2020/10/Interpre%CC%81tation-GPAQ.pdf).
