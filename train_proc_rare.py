import sys

def replace_rare(training_name):
    '''
    '''
    rare_name = ( training_name.split(".") )[0]+"_rare.train"

    rare_dict = {}
    with open(training_name, "rb") as src:
        l = src.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ") 
                word = fields[0]
                if rare_dict.has_key(word):
                    rare_dict[word] += 1
                else:
                    rare_dict[word] = 1
            l = src.readline()

    with open(training_name, "rb") as src, open(rare_name, "w") as targ:
        l = src.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ") 
                word = fields[0]
                tag = fields[1]
                key = (tag,word)
                if rare_dict[word] < 5:
                    targ.write("_RARE_" + " " +  tag + "\n")
                    #print key
                else:
                    targ.write(word + " " +  tag + "\n")
                    #targ.write( l )
            else:
                targ.write("\n")
            l = src.readline()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
       replace_rare(sys.argv[1])



    
    
