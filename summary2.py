import openai
from subprocess import Popen, PIPE
import re
import json

# 발급받은 API 키 설정
OPENAI_API_KEY = "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"
openai.api_key =  OPENAI_API_KEY
model = "babbage-002"


## content를 json 파일로 읽어서 가져와야해 
file = 'RFP2.hwp'
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
partial_json_data_str3 = json_data_str[end_index+4097:]


# Setting up the conversation for ChatGPT
messages = [
     {"role": "system", "content": "사업규모, 사업기간, 사업명, 제안기관, 추진일정, 문의처에 대해 간략하게 요약해주고 과업 내용은 \
      세부적으로 요약을 해주고,과업 내용 요약을 할 떄는 단락을 나누는 것 없이 띄어쓰기 만으로 한 줄 안으로 요약을 해줘 과업 내용은 꼭 넣어줘"},
     {"role": "user", "content": partial_json_data_str1}
]
messages2 = [
    {"role": "system", "content": "제안 요청에 대분류, 소분류로 나눠서 요약해주는 대신 단락을 나누는 것 없이 띄어쓰기 만으로 한 줄 안으로 요약을 해줘 과업 내용은 꼭 넣어줘 "},
     {"role": "user", "content": partial_json_data_str2}
]
messages3 = [
    {"role": "system", "content": "대분류, 소분류로 나눠서 요약해주는 대신 단락을 나누는 것 없이 띄어쓰기 만으로 한 줄 안으로 요약을 해줘 과업 내용은 꼭 넣어줘"},
     {"role": "user", "content": partial_json_data_str3}
]
response = openai.ChatCompletion.create(model=model, messages=messages)
summary1 = response['choices'][0]['message']['content']

response = openai.ChatCompletion.create(model=model, messages=messages2)
summary2 = response['choices'][0]['message']['content']

response = openai.ChatCompletion.create(model=model, messages=messages3)
summary3 = response['choices'][0]['message']['content']



summaries_dict = {
    "summary1": summary1,
    "summary2": summary2,
    "summary3": summary3
}
print("summaries_dict",summaries_dict)

processed_summaries = {}

for key, value in summaries_dict.items():
    # Initialize dictionary to store key-value pairs for this summary
    summary_dict = {}

    # If the value is a single line, treat it as a key with the rest as the value
    if '\n' not in value:
        print("not value \n",value)
        summary_dict[key] = value.strip()

    if '\n' not in value and ':' in value:
        parts = section.split(":",1)
        key, value = parts
        summary_dict[key.strip()] = value.strip()
    else:
        # Split summary into sections
        sections = re.split(r'\n\n', value)

        # Iterate over sections and extract key-value pairs
        for section in sections:
            # Split section into lines
            lines = section.split('\n')

            # Extract key-value pairs from lines
            for line in lines:
                # Split line into key and value
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    key, value = parts
                    summary_dict[key.strip()] = value.strip()

        # Add extracted key-value pairs to processed_summaries
    processed_summaries[key] = summary_dict

# Display the processed summaries
print("processed_summaries", json.dumps(processed_summaries, ensure_ascii=False, indent=2))

json_file_path = 'summaries_rfp2.json'
txt_file_path = 'summaries.txt'

# Write the dictionary to the JSON file
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(processed_summaries, json_file, ensure_ascii=False)

print(f"Summaries saved to {json_file_path}")

