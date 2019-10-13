import requests
import pickle
from bs4 import BeautifulSoup

# Parameters:
# set=pmc-open: Subset for which full text may be harvested
# verb=ListRecords: Fetch the records
# metadataPrefix=pmc: Get full text
base_url = 'https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?set=pmc-open&verb=ListRecords&metadataPrefix=pmc'
url = base_url
num_processed = 1

try:
    while True:
        print('Processing #' + str(num_processed))
        response = requests.get(url)

        xml = BeautifulSoup(response.text)
        records = xml.html.body.listrecords

        abstracts = [x.text for x in records.find_all('abstract')]
        texts = [x.text for x in records.find_all('sec')]

        with open('abstracts-' + str(num_processed) + '.pkl', 'wb') as f:
            pickle.dump(abstracts, f)

        with open('texts-' + str(num_processed) + '.pkl', 'wb') as f:
            pickle.dump(texts, f)
    
        num_processed += 1
        url = base_url + '&resumptionToken=' + records.resumptiontoken.text
except:
    print('Failed: error below.')
    raise

