import pandas as pd
from Bio import Entrez
from bs4 import BeautifulSoup as bs
sdf = pd.read_excel("Supplementary_Table_S3_NEW.xlsx")
#reformat the dataframe and save in a text format
cols = sdf.columns.to_list()
index = cols.index("id_country_date")
cols[0] = 'id_country_date'
cols[index] = 'order'
sdf[cols].to_csv("zika_metadata.csv",index=False)
lookup = sdf.set_index("id").id_country_date.to_dict()
#download the data, using the lookup to swap accessions for the newick-based naming
print("Downloading reference fasta KJ776791...")
with open("zika_reference.fasta",'w+') as of:
    uid_record = Entrez.read(Entrez.esearch(db='nuccore', retstart=0, retmax=1, term="KJ776791", retmode='xml'))
    dhandle=Entrez.efetch(db='nuccore', id=uid_record['IdList'], retmode='xml') 
    genome_record = bs(dhandle.read(),'xml')
    dhandle.close()
    print(genome_record.find("GBSeq_primary-accession").text)
    print(">"+genome_record.find("GBSeq_primary-accession").text,file=of)
    print(genome_record.find("GBSeq_sequence").text.upper(),file=of)
print("Downloading sample data...")
with open("zika_S3.fasta",'w+') as of:
    for sid in sdf.id:
        print(f"Fetching sequence of {sid}...")
        uid_record = Entrez.read(Entrez.esearch(db='nuccore', retstart=0, retmax=1, term=sid, retmode='xml'))
        dhandle=Entrez.efetch(db='nuccore', id=uid_record['IdList'], retmode='xml') 
        genome_record = bs(dhandle.read(),'xml')
        dhandle.close()
        name = genome_record.find("GBSeq_primary-accession").text
        print(">"+lookup.get(name, name+"_MISSING"),file=of)
        print(genome_record.find("GBSeq_sequence").text.upper(),file=of)