while True:
    marker_symbol = input("Please enter a gene symbol: ")
    if any(x.isspace() for x in marker_symbol):
        print("No spaces allowed, please re-enter.")
        continue

    if not all(x.isalnum() for x in marker_symbol):
        print("Alphanumeric only please.")
        continue

    import pandas as pd
    CSV_URL = "https://www.ebi.ac.uk/mi/impc/solr/genotype-phenotype/select?q=marker_symbol:" + marker_symbol + "&rows=500&wt=csv&indent=1"
    df = pd.read_csv(CSV_URL)

    if df.empty:
        print("Looks like that gene doesn't have available information. Try another gene or check your cAsE.")
        continue
    else:
        break
AlleleFound = pd.unique(df['allele_symbol']).tolist()
AlleleFound = str(AlleleFound)
print("IMPC found this allele: " + AlleleFound)
df = df.dropna(subset=['percentage_change'])
print(pd.unique(df['mp_term_name']).tolist())
PhenoTerm = input("Select a phenotype for analysis:  ")
ParamId4Query = df.loc[df['mp_term_name'] ==  PhenoTerm, "parameter_stable_id"].iloc[0]
ColonyId4Query = df.loc[df['mp_term_name'] ==  PhenoTerm, "colony_id"].iloc[0]

CSV2_URL =  "https://www.ebi.ac.uk/mi/impc/solr/experiment/select?q=parameter_stable_id:"+ ParamId4Query +"%20AND%20colony_id:" + ColonyId4Query + "&rows=500&wt=csv&indent=true"
df2 = pd.read_csv(CSV2_URL) # this is KO data
MetadataGroupID = df2['metadata_group'].iloc[0]
PhenoCenterID = df2['phenotyping_center'].iloc[0]
ControlDataURL = "https://www.ebi.ac.uk/mi/impc/solr/experiment/select?q=parameter_stable_id:" + ParamId4Query + "&wt=csv&fq=metadata_group:" + MetadataGroupID + "&fq=phenotyping_center:" + PhenoCenterID + "&fq=strain_accession_id:%22MGI:2159965%22&fq=biological_sample_group:control&rows=100"
df3 = pd.read_csv(ControlDataURL) # this is wildtype data
#print(df3.info())
frames = [df2, df3]
df4 = pd.concat(frames)
#print(df4.info())
df4.groupby(['biological_sample_group', 'sex'])[['data_point']].mean()
import matplotlib.pyplot as plt
x = df4['date_of_experiment']
y = df4['data_point']
plt.scatter(x,y) #color by "biological_sample_group" < need to be a factor??
plt.show()
import seaborn as sns
x = df4['date_of_experiment']
y = df4['data_point']
sns.catplot(x = 'sex', y = 'data_point', col = 'biological_sample_group', kind = 'bar', data=df4)
plt.show()
