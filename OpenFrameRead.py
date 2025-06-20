file1 = open("data.txt")
file2 = open("RNA_codon_table.txt")

count = 0

file2 = open("RNA_codon_table.txt")
RNAtoAA ={}
for line in file2:
    line = line.strip()
    RNAtoAA[line[0:3]] = line[4:8]
    
sequences =[]
count = 0
for line in file1:
    line = line.strip()
    if line.find("Rosalind") == -1:
        line = line.replace("T", "U")
        sequences = sequences + [line]

string = ''.join([i for i in sequences])

CompString=list(string)
for i in range(len(string)):
    if string[i]=='A':
        CompString[len(string)-1-i] = 'U'
    elif string[i]=='U':
         CompString[len(string)-1-i] = 'A'
    elif  string[i]=='G':
         CompString[len(string)-1-i] = 'C'
    else:
         CompString[len(string)-1-i] = 'G'
RevCompString = ''.join(CompString)

def OpenReadFrame(string, RNAtoAA):  
    protein =[]
    for i in range(len(string)-3):
        if RNAtoAA[string[i:i+3]] == 'M':
            for j in range(i, len(string)-3,3):
                print(j)
                protein.append(RNAtoAA[string[j:j+3]])
                if RNAtoAA[string[j:j+3]] == 'Stop':
                    break
           
    length = protein.count('Stop')
    ProteinString =[""]*length
    count = 0
    for i in range(len(protein)):
        if protein[i] != 'Stop':
             ProteinString[count]+=protein[i]
        elif count == len(ProteinString)-1:
            break
        else:
            count+=1
            
        

    return ProteinString
                
result = list(set(OpenReadFrame(string, RNAtoAA) + OpenReadFrame(RevCompString, RNAtoAA)))

with open("Protein.txt", 'w') as f:
    for i in range(len(result)):
        f.write(result[i]+'\n')

print(result)
          
              
           
            
