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

