import openai
from subprocess import Popen, PIPE
import json
import re
import dotenv
import os

# Set your OpenAI API key
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

def get_openai_response(model, user_role, user_content, RFP):
    print("API 호출 중")
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": user_role},
            {"role": "user", "content": user_content},
            {"role" : "assistant", "content":RFP}
        ]
    )
    return completion['choices'][0]['message']['content']

def process_info_string(info_string):
    # Remove brackets and split the string based on commas
    
  
    info_list = []
    sum_value = ''

    for item in info_string.split(','):
        item = item.strip(" '[]")
        # Check if all characters in the string are digits
        if item.isdigit() or (item.startswith("0") and '원' in item):
            sum_value += item
        elif (not item.isdigit()) and sum_value != '':
            info_list.append(sum_value)
            info_list.append(item)
            sum_value = ''
        else:
            info_list.append(item)

    # Append the remaining sum_value if any
    if sum_value:
        info_list.append(sum_value.strip(" '[]"))

    # Remove empty strings from the list
    info_list_cleaned = [item for item in info_list if item]
    
    return info_list_cleaned


def create_json_dict(info1, info2, info3,info4):
    # Process each info string


    info1_list = process_info_string(info1)
    info2_list = process_info_string(info2)
    info3_list = process_info_string(info3)
    info4_list = process_info_string(info4)


# Use regex to split based on numbers in parentheses

    # Separate each item into a list

    # Create a dictionary
    json_dict = {
        "info": {
            "company": info1_list[0],
            "cost": info1_list[1],
            "title": info1_list[2]
        },
        "summary": {
            "start_date" : info4_list[0],
            "end_date":info4_list[1],
            "subject": info2_list,
            "requirement": info3_list
        }
    }

    return json_dict


# Read HWP content from file

def fine_tuning_summary(*rfp_files):
    for rfp_file in rfp_files:
        
        process = Popen(['hwp5txt', rfp_file], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        data = stdout.decode('utf-8')

        rfp_name = rfp_file.split('/')[2].split(".")[0]

        # Verify that 'data' is not empty before proceeding
        if rfp_name:
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

            if "RFP" in rfp_file:
            # Define questions
                question = "정보 ( 제안기관, 비용, 제목에 대해 알려줘 )"
                question2 = "제안요청서에 대한 주제에 대해 알려줘"
                question3 =  "과업의 수행 지침 내에 있는 내용들 알려줘"
                question4 =  "시작일과 마감일에 대해 알려줘"
            # Call the OpenAI API for each question for RFP1
                info1 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8qK0FcdU", "RFP1", question,partial_json_data_str1)
                info2 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8qK0FcdU", "RFP1", question2,partial_json_data_str1)
                info3 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8qK0FcdU", "RFP1", question3,partial_json_data_str2)
                info4 = get_openai_response("ft:gpt-3.5-turbo-1106:personal::8qK0FcdU", "RFP1", question4,partial_json_data_str1)

                # Continue with the rest of your logic or save the data to a file for RFP1
                resulting_json_dict = create_json_dict(info1, info2, info3, info4)

            # Specify the file path for RFP1
                output_file_path = f"./summary/output_{rfp_name}.json"
        

            # Continue with the rest of your logic or save the data to a file
        resulting_json_dict = create_json_dict(info1, info2, info3, info4)

        # Specify the file path
        output_file_path = f"./summary/output_{rfp_name}.json"

        # Save the dictionary to a JSON file
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(resulting_json_dict, json_file, ensure_ascii=False, indent=2)

        print(f"JSON data for {rfp_name} has been saved to {output_file_path}")

if __name__ == "__main__":
    fine_tuning_summary("./RFP/RFP1.hwp", "./RFP/RFP2.hwp")
