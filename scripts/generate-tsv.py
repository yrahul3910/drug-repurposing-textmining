import json

with open('../extracted.json', 'r') as f:
    extracted = json.load(f)

tsv = '\n'.join(list(map(lambda x: x['transcript'], extracted)))

with open('../biobert-data/extracted.tsv', 'w') as f:
    f.write(tsv)
