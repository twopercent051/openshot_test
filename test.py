import json

json_direct = 'openshot.json'
with open(json_direct, 'r') as f:
    item_dict = json.loads(f.read())

result = item_dict['clips'][0]['effects'][0]
clip_json = '{"effects": ' + str(result).replace("'", '"') + '}'

print(clip_json)