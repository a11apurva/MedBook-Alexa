g=open("json-medicines.txt","w")

med_set=set()

for line in open("medicineName.txt","r"):
    line=line.strip()
    line=line.lower()
    words=line.split()
    line=[]
    for i in range(len(words)):
        if i==0:
            line.append(words[i])
            continue
        if words[i].isalpha():
            line.append(words[i])
        else:
            break

    line=" ".join(line)
    med_set.add(line)
    if ("-" in line):
        med_set.add(line.replace("-"," "))
        med_set.add(line.replace("-",""))


for med in sorted(med_set):    
    print med
    g.write("                        {\n")
    g.write("                            \"name\": {\n")
    strx = "                                \"value\": \"{}\"\n".format(med)
    g.write(strx)
    g.write("                            }\n")
    g.write("                        },\n")

g.close()
