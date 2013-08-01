#copy and paste this into your bash console
#make sure to change the ".fna" parts to the extension you want to work with

for file in *.fna; do 
    mkdir $(basename $file .fna);
    cp $file $(basename $file .fna);
done

