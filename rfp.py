import re

info = "['국립국어원 어문연구실 한국어진흥과', '450,000,000원(부가세 포함)', '2022년 개방형 한국어 통합 사전 시스템 클라우드 전환'"


# Remove empty strings from the list


info_list = []
sum_value = ''

for item in info.split(','):
    item = item.strip(" '[]")
    # Check if all characters in the string are digits
    print("item", item)
    if item.isdigit() or (item.startswith("0") and '원' in item):
        print("item2", item)
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
print("info_list_cleaned", info_list_cleaned)