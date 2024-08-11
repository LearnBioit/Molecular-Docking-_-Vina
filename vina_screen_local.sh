#! /bin/bash

for f in ZINC *.pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    C:/cygwin64/home/vina/vina --config conf.txt --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done