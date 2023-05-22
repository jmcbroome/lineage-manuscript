This folder contains code and scripts for replicating the supplementary analysis of lineage stability.

Dependencies of these scripts are included in the env.yml in this folder. Additionally, you will need [Autolin](https://github.com/jmcbroome/autolin) with its own environment and dependencies.

```conda env create -f env.yml```

Detailed replication information can be found in the Lineage Stability Analysis notebook. Relevant commands are replicated below:

```
wget http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/2023/03/30/public-2023-03-30.all.masked.pb.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/2023/03/30/public-2023-03-30.metadata.tsv.gz
mv public-2023-03-30.metadata.tsv.gz public-2023-03-30.all.masked.metadata.tsv.gz
snakemake --cores 1 --snakefile flag_lineages.smk public-2023-03-30.all.masked.proposed.pb
matUtils summary -i public-2023-03-30.all.masked.proposed.pb -C auto_proposed_sample_clades.txt
for f in public-2023-04*pb.gz ; do python3 clean_lineages.py -a auto_proposed_sample_clades.txt -t $f ; done
awk -F'\t' '{print $2"\t"$1}' auto_proposed_sample_clades.txt > auto_proposed_clades_samples.txt
matUtils extract -i public-2023-03-30.all.masked.proposed.pb -C auto_proposed_clade_paths.txt
awk -F'\t' '{print $1"\t"$3}' auto_proposed_clade_paths.txt > auto_proposed_clade_paths.cleaned.txt
annotation_loop.sh
for f in cleaned*transfer.pb.gz ; do echo $f ; matUtils summary -i $f -C ${f%pb.gz}cladesamples.txt ; done
```

Then open the notebook in Jupyter and run the code inside.