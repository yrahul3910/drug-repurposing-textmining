# Files

* `extracted.json`: The excerpts with confidence above 96%.
* `reports/`: All reports produced, in Markdown and PDF formats.
* `Transcripts/`: The NPR transcripts data
* `papers/`: Relevant papers
* `scripts/`: Any scripts used.
* `drug-names.txt`: List of drug names from DrugBank. This was used as a dictionary to perform a naive string match to check how many of these are in the NPR dataset.
* `biobert/`: Code for the BioBERT model
* `biobert-data/`: Data formatted for BioBERT (`test.tsv`), along with some preprocessed datasets provided by BioBERT authors (`NERdata/`), and a development set taken from one of those datasets (`devel.tsv`)
* `pretrained/`: Pretrained BioBERT model
* `bioflair/`: The BioFLAIR code and data, with small tweaks. Code from [this repo](https://github.com/shreyashub/BioFLAIR)
* `bioflair-trained/`: The trained BioFLAIR model, for 81 epochs on the `bc5cdr` dataset.
