import yaml  # pip install pyyaml

# Open the YAML file and read the content
with open('settings/promts.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Now you can use 'data' as a normal Python dictionary
print(data)
