# compresses a folder of vtp files!
for i in *
do
  tko="${i/%.vtp/.tko}"
  trakofy -i $i -o $tko
done