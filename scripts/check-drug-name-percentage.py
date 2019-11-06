import pandas as pd
import os

df = pd.read_csv('drug-names.txt', sep='\t')
drugs = list(df['Name'])

# Count average statistics
word_count = 0
word_count_unique = 0
count = 0
count_unique = 0

# Count drug statistics
final_bag = set()
drugs_used = 0

# Files processed
counter = 0

for filename in os.listdir('./Transcripts/RAW'):
    with open('./Transcripts/RAW/' + filename, 'r', encoding='iso-8859-1') as f:
        counter += 1
        print('(', str(counter), '/', str(len(os.listdir('./Transcripts/RAW'))), ') Processing', filename)
        text = f.read()
        words = text.split()
        bag = set(words)
        final_bag = final_bag.union(bag)

        word_count += len(words)
        word_count_unique += len(bag)

        for drug in drugs:
            if drug in words:
                count += 1
            if drug in bag:
                count_unique += 1

for drug in drugs:
    if drug in final_bag:
        drugs_used += 1


text_in_db = round(count / word_count * 1e4) / 100
uniq_text_in_db = round(count_unique / word_count_unique * 1e4) / 100
drugs_used_percent = round(drugs_used / len(drugs) * 1e4) / 100
print(str(text_in_db) + '% of the total text is drugs in the database.')
print(str(uniq_text_in_db) + '% of the unique words in the data are drugs in the database.')
print(str(drugs_used_percent) + '% of the drugs exist in the text.')

