# 1) Search IMPC database by gene symbol to retrieve a phenotype
#       get user input and formulate http query via API
#       parse phenotypes out of dataframe
#       guide user to select phenotype of continuous data only???

# 2) Search IMPC database by phenotype term & colony to retrieve experimental data
#        get user input and formulate http query via API

# 3) Need a way to retrieve more control data?

# 4) manipulate dataframe to clean data
#        generate some summary stats?
#        print out boxplot  by genotype (wild type versus mutant) separated by sex
#        print out similar scatter plot?

# continuous data, categorical data, time series data, image data
# An input is requested (gene symbol) and stored in a variable


import pandas as pd

while True:
    marker_symbol = input("Please enter a gene symbol: ")
    if any(x.isspace() for x in marker_symbol):
        print("No spaces allowed, please re-enter.")
        continue

    if not all(x.isalnum() for x in marker_symbol):
        print("Alphanumeric only please.")
        continue
    else:
        break

import pandas as pd

CSV_URL = "https://www.ebi.ac.uk/mi/impc/solr/genotype-phenotype/select?q=marker_symbol:" + marker_symbol + "&rows=500&wt=csv&indent=1"
df = pd.read_csv(CSV_URL)
AlleleFound = pd.unique(df['allele_symbol']).tolist()
AlleleFound = str(AlleleFound)
print("IMPC found this allele: " + AlleleFound)

CSV_URL = "https://www.ebi.ac.uk/mi/impc/solr/genotype-phenotype/select?q=marker_symbol:" + marker_symbol + "&rows=500&wt=csv&indent=1"
df = pd.read_csv(CSV_URL)
# Do some more error checking at this stage!! Confirm that the correct gene is returned.
AlleleFound = pd.unique(df['allele_symbol']).tolist()
AlleleFound = str(AlleleFound)
print("IMPC found this allele: " + AlleleFound)

#df1 = df.dropna(subset=['percentage_change']) < that seems to work!
if df.empty:
    print("Looks like that gene doesn't have available information. Try another gene or check your cAsE.")
    # return to beginning
else:
    Dec = input("Proceed? Yes or Re-enter:")
    if Dec == Proceed:
        continue

    else:
        return to beginning


# if Y then continue, if Re-enter then return to top

pd.unique(df['mp_term_name']).tolist()

PhenoTerm = input("Select a phenotype for analysis:  ")

#Use the mp_term_name to then retrieve the procedure ID and Colony_Id by filtering/slicing the dataframe:

ParamId4Query = df.loc[df['mp_term_name'] ==  PhenoTerm, "parameter_stable_id"].iloc[0]

#print(ParamId4Query)
# 'IMPC_HEM_002_001'

ColonyId4Query = df.loc[df['mp_term_name'] ==  PhenoTerm, "colony_id"].iloc[0]
# print(ColonyId4Query)
#  'MEBV'

#ALTERNATIVE - use filter "fl" in the query to get back parameter ID and colony
#this URL works fine in browser but not in python console: (white space argghhh)

#testurl = "https://www.ebi.ac.uk/mi/impc/solr/genotype-phenotype/select?q=marker_symbol:Fbxo7%20AND%20mp_term_name:decreased\ hematocrit&rows=1&wt=csv&indent=true&fl=parameter_stable_id,colony_id"
#returns this:
#parameter_stable_id,colony_id
#IMPC_HEM_002_001,MEBV

#combine parameter ID and Colony name to get the experimental data for plotting! now the http points to "experiment"

CSV2_URL =  "https://www.ebi.ac.uk/mi/impc/solr/experiment/select?q=parameter_stable_id:" + ParamId4Query + "%20AND%20colony_id:" + ColonyId4Query + "&rows=500&wt=csv&indent=true"
print(CSV2_URL)
#insert rows=500 to be sure to get more than 10 rows! This *should* return all the KOs (14?) this http request pulls down the experimental data
#how to retrieve more controls (this only gets colony littermate controls)?

#getting littermate controls means collecting "metadata_group" info and "phenotyping_center" info to send another query

ControlURL = "https://www.ebi.ac.uk/mi/impc/solr/experiment/select?q=parameter_stable_id:IMPC_HEM_002_001%20AND%20colony_id:MEBV&indent=true&wt=csv&rows=1&fl=metadata_group,phenotyping_center,strain_accession_id"
#this returns only the "metadata_group" info and "phenotyping_center" "strain_accession_id" info
#how does this FL thing work???  fl=metadata_group,phenotyping_center,strain_accession_id

#take the info in ControlURL to formulate the request for control data...

ControlDataURL = "https://www.ebi.ac.uk/mi/impc/solr/experiment/select?q=parameter_stable_id:IMPC_HEM_002_001&wt=csv&fq=metadata_group:c5d5b3349a0014cdac742fb284d786ed&fq=phenotyping_center:WTSI&fq=strain_accession_id:%22MGI:2159965%22&fq=biological_sample_group:control&rows=100"
# using metadata_group & phenotyping_center & parameter ID to retrieve 100 rows of control data

#read in the CSV files and do some analysis + plots
import pandas as pd
df2 = pd.read_csv(CSV2_URL)
df2.info()

df3 = pd.read_csv(ControlDataURL)
df3.info()

#report that there are x sample in two groups - control & exp.?

#check that data_point and weight are FLOAT?



#Now do some analysis + plots
#report the summary stats? see below...

# df2[df2['biological_sample_group']  == 'experimental']
# selects the knockouts only

# use groupby to group exp vs control and male vs female, calculate mean for each group
#grouped = df2['data_point'].groupby([df2['biological_sample_group'], df2['sex']])
#grouped.mean()
# string together the mean method
#df2['data_point'].groupby([df2['biological_sample_group'], df2['sex']]).mean()
#further simplify the code to do this analysis

df2.groupby(['biological_sample_group', 'sex'])[['data_point']].mean()

#how to pass this along to the plot functions?

#seems like a whisker plot can be generated directly from the group object

#scatter plot of values in the 4 groups - put those into 4 variables????
# need color or shape to show M vs F and KO vs WT

import matplotlib.pyplot as plt
x = df2['date_of_experiment']
y = df2['data_point']
plt.scatter(x,y)
plt.show()
#how to do a scatterplot and color and shape the 4 groups ??


#here is column plot of KO vs WT grouped by sex
import seaborn as sns
x = df2['date_of_experiment']
y = df2['data_point']
sns.catplot(x = 'sex', y = 'data_point', col = 'biological_sample_group', kind = 'bar', data=df2)
plt.show()


# does not have mut vs wt
# any reason to show weight?
#sns.violinplot(x = 'sex', y = 'weight', col = 'biological_sample_group', kind = 'violin', data=df2)
#plt.show()
