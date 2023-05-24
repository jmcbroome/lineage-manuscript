This folder contains code and data to replicate an application of Autolin to Seabra et al's Zika phylogeny and associated lineage system.

First, obtain the [Supplementary Table S3](https://academic.oup.com/ve/article/8/1/veac029/6555351#351081937) online and save it to this directory. Then run our Entrez-based download script- `python3 download_zika_sequences.py`. This script parses this table, saves a csv with reordered columns, and produces both a fasta for the reference used in Seabra et al and a fasta containing the sequences of all samples mentioned in Supplementary Table S3. The newick itself can be obtained by contacting the corresponding authors directly.

Once the reference and sequences are available, a protobuf can be produced using [our pipeline](https://github.com/jmcbroome/pathogen-protobuf). Edit the configuration file so that the reference variable matches the name of your reference fasta file. 

```
snakemake -c1 zika_S3.pb
```

For maximum comparability, however, we apply mutation annotations to the tree inferred by Seabra et al. To accomplish this, you can stop at the VCF step and combine this VCF with a newick file for those samples using UShER.

```
snakemake -c1 zika_S3.vcf
usher -t seabra_zika.nwk -v zika_S3.vcf -o seabra_zika.pb -l
```

You can then annotate the protobuf with [Autolin](https://github.com/jmcbroome/autolin/blob/main/propose_sublineages.py). The -t and -f parameters should be set to 0 if using branch lengths with a value <1.

```
python3 propose_sublineages.py -i seabra_zika.pb.gz -o seabra_zika.autolin.pb -l seabra_zika.labels.txt -m 3 --recursive -t 0 -f 0
```

From the protobuf, an Auspice JSON can be extracted and annotated.

```
matUtils extract -i seabra_zika.pb -j seabra_zika.json -M zika_metadata.csv
```

Our ARI analysis can be found in the included Jupyter notebook.