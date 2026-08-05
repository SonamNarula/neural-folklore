import os

# Get the current working directory
path = os.getcwd()

# Print all files and folders in the directory
contents = os.listdir(path)

print("Contents of the directory:")
for item in contents:
    print(item)