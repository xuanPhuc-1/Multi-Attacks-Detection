#!/bin/bash
for i in {1..2000}
do
    # extract essential data from raw data
    sudo ovs-ofctl dump-flows s2 > data/raw.txt
    grep "nw_src" data/raw.txt > data/flowentries.csv
    packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/flowentries.csv)
    bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/flowentries.csv)
    ipsrc=$(awk -F "," '{split($15,c,"="); print c[2]","}' data/flowentries.csv)    #14 cho l3
    ipdst=$(awk -F "," '{split($16,d,"="); print d[2]","}' data/flowentries.csv)    #15 cho l3
    # ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($15,d,"="); print d[2]","}')
    # ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($16,d,"="); print d[2]","}')
    # inport=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/flowentries.csv | awk -F " " '{split($10,d,"="); print d[2]","}')
    # check if there are no traffics in the network at the moment.
    if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst" 
    then
        state=0
    else
        echo "$packets" > data/packets.csv
        echo "$bytes" > data/bytes.csv
        echo "$ipsrc" > data/ipsrc.csv
        echo "$ipdst" > data/ipdst.csv
            
        state=$(awk '{print $0;}' result.txt)
    fi
    # echo "State is $state"
    python3 computeTuples.py
    python3 inspector.py

    if [ $state -eq 1 ];
    then
        echo "Network is under attack"
    else
        echo "Network is normal"
    fi

    sleep 3
done



# ==============================================================================================================================================
# Ref
# Get all fields (n columns) in awk: https://stackoverflow.com/a/2961711/11806074
# e.g. awk -F "," '{out=""; for(i=2;i<=NF;i++){out=out" "$i" "i}; print out}' data/flowentries.csv 

# ovs-ofctl reference
# add-flow SWITCH FLOW        add flow described by FLOW    e.g. ... add-flow s1 "flow info"
# add-flows SWITCH FILE       add flows from FILE           e.g. ... add-flows s1 flows.txt

# example of multiple commands in awk, these commands below extract ip_src and ip_dst from flow entries
# awk -F "," '{split($10,c,"="); print c[2]","}' data/flowentries.csv > data/ipsrc.csv
# awk -F "," '{split($11,d,"=");  split(d[2],e," "); print e[1]","}' data/flowentries.csv > data/ipdst.csv
