g=open("json-diseaes.txt","w")

disease_set=set()

for line in open("diseasename.txt","r"):
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
    disease_set.add(line)

for disease in sorted(disease_set):    
    print disease
    g.write("                        {\n")
    g.write("                            \"name\": {\n")
    strx = "                                \"value\": \"{}\"\n".format(disease)
    g.write(strx)
    g.write("                            }\n")
    g.write("                        },\n")

g.close()
