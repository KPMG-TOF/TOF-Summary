import openai
from subprocess import Popen, PIPE
import re
import json

# 발급받은 API 키 설정
OPENAI_API_KEY = "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"
openai.api_key =  OPENAI_API_KEY
model = "gpt-3.5-turbo-1106"


training_response = openai.File.create(
    file=open("example.jsonl", "rb"),
    purpose='fine-tune'
)

training_file_id = training_response["id"]

print("Training file id:", training_file_id)
