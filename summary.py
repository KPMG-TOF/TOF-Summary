import openai
from subprocess import Popen, PIPE
import re
import json

# 발급받은 API 키 설정
OPENAI_API_KEY = "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"

# openai API 키 인증
openai.api_key =  OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"


## content를 json 파일로 읽어서 가져와야해 

file = 'RFP.hwp'
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


# Setting up the conversation for ChatGPT
messages = [
     {"role": "system", "content": "사업규모, 사업기간에 대해 간략하게 요약해주고 과업 내용에 대해서는 안에 세부적인 내용까지 자세하게 요약해줘"},
     {"role": "user", "content": partial_json_data_str1}
]


# Call ChatGPT API2

partial_json_data_str2 = json_data_str[end_index:end_index+4097]



messages2 = [
    {"role": "system", "content": "과업의 수행 지침 내에 있는 (1) 품질보증 계획 제시\
            (2) 통제 및 위험관리 계획 제시\
            (3) 기밀보안 및 비상대책\
            (4) 계약의 이행\
            (5) 과업 성과제출 내용도 자세하게 요약해줘\ "},
     {"role": "user", "content": partial_json_data_str2}
]
partial_json_data_str3 = json_data_str[end_index+4097:]

messages3 = [
    {"role": "system", "content": "요약해서 알려줘 "},
     {"role": "user", "content": partial_json_data_str3}
]



response = openai.ChatCompletion.create(model=model, messages=messages)
summary1 = response['choices'][0]['message']['content']

response = openai.ChatCompletion.create(model=model, messages=messages2)
summary2 = response['choices'][0]['message']['content']

response = openai.ChatCompletion.create(model=model, messages=messages3)
summary3 = response['choices'][0]['message']['content']

print("summary",summary1)
print("summary", summary2)
print("summary",summary3)
