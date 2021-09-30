template for docx file (raport) is from Sabina.
we have colaborated a bit with non-code related stuff such as step data.
my code is my own, appart from the parts that were given by the teacher

to run the program, merely make sure you have:

python 3.8.1,
numpy,
matplotlib and
pandas
and run "stepcounter.py".

you should get the anserws in your console as to how many steps the algorithm thinks the data has. plots for each datapoint are also shown.

the plots show the magnitude of the data in each file in blue, and each step is shown as a black spike in the graph.
the black spikes show what the treshold according to the dynamic algorithm was when it was bypassed.


to run your own data you can for example change the contents of the variable "datafiles" in the main method to add any filepath or just reuse one of the .csv files that allready are in the folder.
PLEASE OBSERVE: in the programs current form (to make pandas work) you have to add the following row as the first row in your CSV file:
timestamps,x_array,y_array,z_array
