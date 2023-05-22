d=2023-04-01
while [ "$d" != 2023-05-01 ]; do 
  year=$(date -j -f "%Y-%m-%d" $d +%Y)
  month=$(date -j -f "%Y-%m-%d" $d +%m)
  day=$(date -j -f "%Y-%m-%d" $d +%d)
  tree="public-"$d".all.masked.pb.gz"
  wget http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/$year/$month/$day/$tree
  metadata="public-"$d".metadata.tsv.gz"
  wget http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/$year/$month/$day/$metadata
  # mac option for d decl (the +1d is equivalent to + 1 day)
 # d=$(date -j -v +1d -f "%Y-%m-%d" $d +%Y-%m-%d)
  d=$(date -I -d "$d + 1 day")
done
