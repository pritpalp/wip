import subprocess
import argparse
from pathlib import Path
import sys
import shlex

# Get an argument from the command line and check if its a valid file
parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)
p = parser.parse_args()

# open the file and read the lines into a list
if p.file_path.exists():
    with open(p.file_path) as f:
        lines = [line.rstrip() for line in f]
else:
    print("Please provide a valid filename for the list of modules")
    sys.exit()

print("Running the plan for these modules: ")
print(lines)

# use the list to create an argument list
module_list = "terraform plan -no-color"
for line in lines:
    module_list = module_list + " -target=module." + line

my_command = shlex.split(module_list)
call_plan = subprocess.run(my_command, stdout=subprocess.PIPE, text=True, check=True)

# lets parse the string now to see what we got back...
print("\n-----------------\n")

# split into multipule lines
chunks = call_plan.stdout.splitlines()
# go through the lines to print only what we want...
for i in chunks:
    print("###" + i.strip())
"""     if "Plan:" in i:
        print("\n" + i.strip() + "\n")
    if "No changes" in i:
        print("\n" + i.strip()+ "\n")
    if "will be updated in-place" in i:
        print("\n" + i.strip())
    if "must be replaced" in i:
        print("\n" + i.strip())
    if "will be created" in i:
        print("\n" + i.strip())
    if "->" in i:
        print(i.strip())
    if " - " in i:
        print(i.strip())
    if " + " in i:
        print(i.strip()) """


def print_this(i):
    switcher=(
        "No changes" : print("\n" + i + "\n")
    )