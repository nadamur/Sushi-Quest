import os

files_to_execute = [
    "characterCustomization.py",
    "main.py",
    "Level_2.py",
    "Level_3.py"
]

for file in files_to_execute:
    print(f"Executing {file}...")
    os.system(f"python {file}")
    print(f"{file} execution completed.")

print("All files executed successfully.")
