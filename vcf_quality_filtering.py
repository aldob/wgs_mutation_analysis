import os

# Create a list of vcf files that are to be filtered
os.chdir("path/to/vcf/files")
files = [fil for fil in os.listdir("./") if fil.endswith(".vcf")]



# Loop through each of the vcf files
for fil in files:
    print(fil)
    # Open the file for reading and a second "fitlered" file for writing
    with open(fil) as vcf, open("filt_"+fil, 'w') as vcf2:

        # Loop through each line in the file to filter each mutation call by quality
        for line in vcf:
            if not line.startswith("#"):
                columns = line.split("\t")

                info = columns[8]

                # If the call contains a ',' then there are multiple alleles at this nucleotide, and therefore each needs to be filtered seperately
                if "," not in columns[5]:

                    # Filter the call based on TLOD and NLOD values about thresholds of 6.3 and 2.2 respectively
                    tlod = float(info.split("TLOD=")[1].split(";")[0])
                    nlod = float(info.split("NLOD=")[1].split(";")[0])
                    # If above threshold write to filtered file
                    if tlod > 6.3 and nlod > 2.2:
                        temp = vcf2.write(line)
                # If there is a ',' then split the different calls up and filter them seperately
                # This also involves recreating the additional information in the line as it looks different when there are multiple alleles
                else:
                    muts = columns[5].split(",")
                    kp1 = columns[10]
                    kp2 = columns[11]
                    tls = info.split("TLOD=")[1].split(";")[0]
                    nls = info.split("NLOD=")[1].split(";")[0]
                    new_muts = []
                    new_tls = []
                    new_nls = []
                    for mut, tl, nl in zip(muts, tls.split(","), nls.split(",")):
                        if float(tl) > 6.3 and float(nl) > 2.2:
                            new_muts.append(mut)
                            new_tls.append(tl)
                            new_nls.append(nl)
                    if new_muts:
                        line = line.replace(",".join(muts), ",".join(new_muts))
                        line = line.replace("TLOD="+tls, "TLOD="+",".join(new_tls))
                        line = line.replace("NLOD="+nls, "NLOD="+",".join(new_nls))
                        for inf in info.split(";"):
                            if "," in inf:
                                newinf = []
                                for mut in new_muts:
                                    indy = muts.index(mut)
                                    newinf.append(inf.split("=")[1].split(",")[indy])
                                if inf.split("=")[0] in ["RPA", "MBQ", "MMQ", "MFRL"]:
                                    newinf.append(inf.split("=")[1].split(",")[-1])
                                line = line.replace(inf.split("=")[1], ",".join(newinf))
                        kpcount = 0
                        for k1, k2 in zip(kp1.split(":"), kp2.split(":")):
                            newkp1 = []
                            newkp2 = []
                            kpcount+=1
                            if kpcount in [2, 3, 5, 6]:
                                for mut in new_muts:
                                    indy = muts.index(mut)
                                    newkp1.append(k1.split(",")[indy])
                                    newkp2.append(k2.split(",")[indy])
                                if kpcount != 3:
                                    newkp1.append(k1.split(",")[-1])
                                    newkp2.append(k2.split(",")[-1])
                                line = line.replace(k1, ",".join(newkp1))
                                line = line.replace(k2, ",".join(newkp2))
                            elif kpcount == 1:
                                mcount = 0
                                newkp2.append("0")
                                for mut in new_muts:
                                    mcount+=1                                
                                    newkp2.append(str(mcount))
                                line = line.replace(k2, "/".join(newkp2))
                        temp = vcf2.write(line)
            # If the line does start with '#' then it is part of the header and is just written to the filtered file as is
            else:
                temp = vcf2.write(line)


