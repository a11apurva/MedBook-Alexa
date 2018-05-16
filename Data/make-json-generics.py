g=open("json-generic.txt","w")

for line in open("genericsName.txt","r"):
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
    
    print line
    g.write("                        {\n")
    g.write("                            \"name\": {\n")
    strx = "                                \"value\": \"{}\"\n".format(line)
    g.write(strx)
    g.write("                            }\n")
    g.write("                        },\n")

g.close()


