# Files

* `01_low_confidence_prune.js`: Removes all excerpts with confidence below 0.96
* `02 - Fetching Data.ipynb`: Notebook to test fetching data
* `03 - Download xml files.py`: Script based on the above to fetch all data
* `check-drug-name-percentage.py`: Computes the percentage of drugs in DrugBank that are in the transcripts dataset.
* `generate-tsv.py`: Generates a .tsv file as required by the BioBERT code.

The second and third are used to fetch data from PubMed Central with the goal of training a Word2Vec model on this.
