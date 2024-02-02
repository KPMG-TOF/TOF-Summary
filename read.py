from subprocess import Popen, PIPE
import json
import re


file = 'RFP.hwp'
process = Popen(['hwp5txt', file], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
data = stdout.decode('utf-8')
print(data)

match = re.search(r'과업 내용(.+)',data)

# Verify that 'data' is not empty before proceeding
if data:
    # Create a dictionary with the 'text' key

    split_data = re.split(r'\n\n', data)
   # Remove lines containing '<표>' and empty strings from the split data
    filtered_data = [line for line in split_data if '<표>' not in line and line.strip() != '']

    # Create a dictionary with the 'text' key
    json_data = {"text":filtered_data}
    
    print("filtered_data", filtered_data)
    # Iterate over the filtered data and use the first part as the key and the rest as the value
    # for item in filtered_data:
    #     parts = item.split('□', 1)
    #     if len(parts) >= 2:
    #         key = parts[0].strip()
    #         value = parts[1].strip()
    #         json_data[key] = value
    # Specify the output JSON file path
    json_file_path = 'output2.json'

    # Write the dictionary to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    print(f"Data written to {json_file_path}")
else:
    print("No data to write to JSON file.")