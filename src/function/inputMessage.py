import json

json_path = ".\..\docs\info.json"

json_dict = json.load(open(json_path, 'r', encoding='utf-8'))

def input_message(message):

    msg = message.replace('\n', '')
    if msg not in json_dict["message"]:
        json_dict["message"].append(message.replace('\n', ''))

    with open(json_path, 'w', encoding= 'utf-8') as f:
        json.dump(json_dict, f, indent=4, ensure_ascii=False)
    return 0