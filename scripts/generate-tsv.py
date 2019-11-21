import json

with open('../extracted.json', 'r') as f:
    extracted = json.load(f)

# Get passages
passages = list(map(lambda x: x['transcript'], extracted))

# Join words by marking them all class B. This is a test file, so we're only
# really adding a random class because the format wants it. In reality, these
# classes are what we want to predict ¯\_(ツ)_/¯
words = '\n'.join(['\tB\n'.join(passage.split()) for passage in passages])

with open('../biobert-data/extracted.tsv', 'w') as f:
    f.write(words)
    f.write('\n')
