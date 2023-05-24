awk '$2 != ""' auto_proposed_clade_paths.cleaned.txt | tail -n +2 > current.auto_proposed_clade_paths.cleaned.txt
cp auto_proposed_clades_samples.txt current.auto_proposed_clades_samples.txt
for f in cleaned*masked.pb.gz ; 
do echo $f ; 
python3 paths_to_sets.py < current.auto_proposed_clade_paths.cleaned.txt > current.auto_proposed_mutation_set.cleaned.txt ;
matUtils annotate -i $f -M current.auto_proposed_mutation_set.cleaned.txt -c current.auto_proposed_clades_samples.txt -o ${f%.pb.gz}.transfer.pb.gz 2> ${f%.pb.gz}.annotate.log;
echo "Transfer complete; updating lineage files" ;
matUtils summary -i ${f%.pb.gz}.transfer.pb.gz -C current.auto_proposed_sample_clades.txt ; 
awk -F'\t' '{print $2"\t"$1}' current.auto_proposed_sample_clades.txt > current.auto_proposed_clades_samples.txt ; 
cp current.auto_proposed_clades_samples.txt ${f%.pb.gz}.day_proposed_clades_samples.txt ;
matUtils extract -i ${f%.pb.gz}.transfer.pb.gz -C current.auto_proposed_clade_paths.txt ; 
awk -F'\t' '{print $1"\t"$3}' current.auto_proposed_clade_paths.txt | awk '$2 != ""' | tail -n +2 > current.auto_proposed_clade_paths.cleaned.txt ; 
cp current.auto_proposed_clade_paths.cleaned.txt ${f%.pb.gz}.day_clade_paths.cleaned.txt ;
done || exit 1

