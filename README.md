# Introduction

The purpose of this script is to generate automatically a markdown for the documentation of an SAP HANA Database project.

Since it's based on the files, one is sure that the documentation reflects the content of the project.

A this stage, "only" the calculated fields are documented. It will generate a markdown with the following structure :
* Subsection : the name of the calculation view
  * Subsubsection (h3) : the label of the calculated columns
    * list of the name of the column, datatype, and where it is created.
    * Replication of the formula typed in the calculationview.

Exemple:

![image](https://user-images.githubusercontent.com/109912854/189488080-cd0ec66d-9250-4745-aad7-f06e00473b13.png)

The text can be either in French (FR) or English (EN). 

# How to use it ?

*Requires python 3.10*

Clone the repo, open a command prompt and execute this statement:
```
python make_doc.py "path of the HDB module"
```




It will scan for all *.hdbcalculationview files in the directory and generate a markdown file at the root of this directory 

# Next steps planned
* List the datasources of the calculationview
* Generate a diagram of the relationships between the entities (tables, synonymes, calculationview) for the project
* Specify where to write the markdown
* Ignore calculationview not in src folder
* Explain how to use this in a pipeline

***Please feel free to submit merge requests to enhence the functionnalities***
