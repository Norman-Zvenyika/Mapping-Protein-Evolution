import re

line = "3PJ6_A|PDB0.14  0.14"
label = re.match(r"(.+\|PDB)", line).group(1)
print(label) # Output: 3PJ6_A|PDB