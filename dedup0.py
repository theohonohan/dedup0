import os.path
import sys
import hashlib

def readnames():
        for line in sys.stdin:
                line = line.rstrip()
                lines = line.split('\x00')
                for line in lines:
                        yield line

filelist = [item for item in readnames()]

files = {}
multiples = {}

for file in filelist:
        if os.path.basename(file) in files:
                multiples.setdefault(os.path.basename(file), [files[os.path.basename(file)]]).append(file) 
        else:
                files[os.path.basename(file)] = file    

number_of_clashing_names = len(multiples)

for matches in multiples.values():
        print()
        match_sums = {}
        for file in matches:
                print(file)
                
                sha1 = hashlib.sha1()

                with open(file, 'rb') as f:
                        while True:
                                data = f.read(524288)
                                if not data:
                                        break
                                sha1.update(data)
                if sha1.hexdigest() in match_sums:      
                        print("Duplicate of", match_sums[sha1.hexdigest()], sha1.hexdigest())
                else:
                        print(sha1.hexdigest())
                        match_sums[sha1.hexdigest()] = file

print()
print(number_of_clashing_names, "sets of identically named files found")
