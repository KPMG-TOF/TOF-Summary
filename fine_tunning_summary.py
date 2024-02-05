import openai
from subprocess import Popen, PIPE
import json
import re

# Set your OpenAI API key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def get_openai_response(model, user_role, user_content):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
            {"role": user_role, "content": user_content}
        ]
    )
    return completion['choices'][0]['message']['content']

def process_info_string(info_string):
    # Remove brackets and split the string based on commas
    info_list = [item.strip(" '[]") for item in info_string.split(',')]
    
    # Remove empty strings from the list
    info_list_cleaned = [item for item in info_list if item]
    
    return info_list_cleaned


def create_json_dict(info1, info2, info3,info4):
    # Process each info string
    info1_list = process_info_string(info1)
    info2_list = process_info_string(info2)
    #info3_list = process_info_string(info3)
    info3_list = info3.strip(" '[]")
    info4_list = process_info_string(info4)

    print("info4_list",info4_list)

# Use regex to split based on numbers in parentheses

    # Separate each item into a list

    # Create a dictionary
    json_dict = {
        "info": {
            # "start_date" : info4_list[0],
            # "end_date" : info4_list[1],
            "company": info1_list[0],
            "cost": info1_list[1],
            "title": info1_list[2]
        },
        "summary": {
            "subject": info2_list,
            "requirement": info3_list
        }
    }

    return json_dict


# Read HWP content from file
file = './RFP/RFP.hwp'
process = Popen(['hwp5txt', file], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
data = stdout.decode('utf-8')

# Verify that 'data' is not empty before proceeding
if data:
    split_data = data.split('\n\n')
    filtered_data = [line for line in split_data if '<표>' not in line and line.strip() != '']

    # Create a dictionary with the 'text' key
    json_data = {'text': filtered_data}

json_data_str = json.dumps(json_data, ensure_ascii=False)
total_length = len(json_data_str)
start_index = 0 
end_index = total_length // 3

partial_json_data_str1 = json_data_str[start_index:end_index]
partial_json_data_str2 = json_data_str[end_index:end_index+4097]

# Define questions
question = "정보 ( 제안기관, 비용, 제목에 대해 알려줘 )"
question2 = "13년 글로벌전략기술개발 RFP 도출을 위한 시장성 평가에 대한 주제에 대해 한국말로 알려줘"
question3 = "과업의 수행 지침 내에 있는 내용들 알려줘"
question4 = "RFP1에 대한 시작일과 마감일에 대해 알려줘"

# Call the OpenAI API for each question
info1 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8oprBlnQ", "user", question)
info2 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8oprBlnQ", "user", question2)
info3 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8oprBlnQ", "user", question3)
info4 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8oprBlnQ", "user", question4)

print("info1:", info1)
print("info2:", info2)
print("info3:", info3)
print("info4:", info4)



# Print the resulting dictionary
resulting_json_dict = create_json_dict(info1, info2, info3, info4)
print(resulting_json_dict)

# Specify the file pa.th
output_file_path = "./summary/output.json"

# Save the dictionary to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(resulting_json_dict, json_file, ensure_ascii=False, indent=2)

print(f"JSON data has been saved to {output_file_path}")
