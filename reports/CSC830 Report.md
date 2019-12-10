# Identifying Novel Treatments for Rare Diseases using Radio Transcripts

### Rahul Yedida

## Abstract

Identifying novel treatments for rare diseases is a difficult medical problem, exacerbated by the few number of cases reported and clinical trials conducted. This document describes an approach using radio transcript data to mine novel treatments for diseases, along with the existing files and code.

## Data

The data is transcripts of a medical radio show, where episodes consist of people describing their experiences living with various diseases. Some episodes discuss specific courses of treatments they took, while others simply discuss different stages of such diseases. It is known that there are no nonsense statements in the audio. This audio was passed to Google Cloud to generate text transcripts.

## Initial approach

I initially proposed a 7-step approach to the problem, after going through the data. For a detailed intuition behind the steps, please refer to, “initial writeup.pdf”.

1. **Low confidence text pruning:** The transcripts are not official, and are simply extracted from MP3 files using Google Cloud. The Google Cloud engine chunks the text, and assigns confidence scores (from 0 to 1). I think a threshold of 0.96 to 0.965 should be reasonable, after going through a few excerpts.

2. **Irrelevant term removal:** In this step, we remove healthcare terms that provide no useful information, such as “medicine”, “healthcare”, “pharmacy”, etc. For example, it is not useful to know that a patient cured symptom X simply by taking “medicine”; it is more helpful to understand the specific medication taken.

3. **Classification:** At this stage, we run a recurrent neural network, such as an LSTM with a one-one structure (i.e., one output for every word, that describes whether it is a medical term or not). The outputs could be binary, or multi-class (drug, disease, or irrelevant).

4. **Speculation removal:** In this stage, we remove speculative phrases, such as “X leads people to do Y”. However, because the transcripts do not have periods, it is difficult to find out where the sentences begin and end. It is possible to instead simply remove the words on either side of such phrases.

5. **Adjacent duplicates removal:** Once we’ve highlighted medical terms that are of interest to us, we wish to form pairs of adjacent important terms. At this stage, we remove adjacent duplicate words.

6. **Pair formation:** Form pairs of adjacent medical terms.

7. **Validation:** Validate the pairs with the help of an expert or a database.

## Modifications to the approach

The approach above has since been largely modified. After a discussion with Daniel, I learned that:

1. The focus is not on the validity of the treatments proposed, since they can be checked. The focus of the project is to simply generate reasonably good pairs; that is, false positives are acceptable, but not false negatives. Therefore, we do not do step 4 above.

2. PubMed is a valuable source of data for training a language model. PubMed is a comprehensive collection of medical papers. PubMed itself only gives access to abstracts, but a subset called [PubMed Central (PMC)](https://www.ncbi.nlm.nih.gov/pmc/tools/ftp/) gives access to the full papers. PubMed has about 28M papers, while PMC has about 2M papers.

3. An alternative to learning the medical terms is to simply use a dictionary file.

4. Yet another alternative is to build a language model to obtain word embeddings and see what terms cluster together—do drugs cluster together? Do diseases cluster together? Are these two distinct clusters?

5. A lot of medical terms are multi-word, which would make the above process a bad idea. [A paper I found later](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7747810) uses this concept to tag the beginning, inside, and outside of medical terms. Their results show that neural networks are not necessarily better than other models, such as Conditional Random Fields (CRFs). Their paper does not link to code, but they seem to imply that passing word embeddings learned by a language model to a CRF may be a good idea.

 

Later, Dr. Chirkova linked me to [BioBERT](https://github.com/dmis-lab/biobert), a language model for medical text. BioBERT is the BERT language model by Google, fine-tuned on PubMed data. BioBERT can perform Named Entity Recognition (NER), which is essentially step 3 in the approach above. After NER, it is trivial to form pairs.

## Code

All code developed is available on [GitHub](https://github.com/yrahul3910/csc830-drug-disease-discovery) (private repository link). Some files have not been committed to the repository. The files are described below:

1. `scripts/01_low_confidence_prune.js`: Removes all excerpts with confidence below 0.96, and generates one JSON file. This creates extracted.json.

2. `scripts/02 - Fetching Data.ipynb`: Jupyter notebook to test fetching data from the server. I like having a notebook to test some part of the code, and then developing a larger notebook/script that does the entire job.

3. `scripts/03 - Download xml files.py`: Script based on the above to fetch all data from the server and parse the resulting XML.

4. `scripts/check-drug-name-percentage.py`: I was asked to check what percentage of the drugs in DrugBank were present in our transcripts data. This file computes all three interpretations of that question. This depends on a file called drug-names.txt.

5. `scripts/generate-tsv.py`: Generates a test.tsv file for the BioBERT model to generate predictions.

### BioBERT

The code in the `biobert/` folders are BioBERT code. Download the BioBERT code from the repo link above, then download their [pre-trained weights](https://github.com/naver/biobert-pretrained). To run their NER code, you need to fine-tune the pre-trained models on your own dataset first, then run predictions. This requires manual labeling, which I have not done yet. Instead, I downloaded their [NER datasets](**https://drive.google.com/open?id=1OletxmPYNkz2ltOr9pyT0b0iBtUWxslh**), and used the `s800` data (I randomly picked this one) to train (you need the `train.tsv` and `train_dev.tsv` files from here). For the `test.tsv` file required, use `generate-tsv.py`.

With these files set up, you can start training the BioBERT model. cd into the directory with the pre-trained weights, and run

```bash
export BIOBERT_DIR=$PWD
```

Next, go to the directory where the different .tsv files are present, and run

```bash
export NER_DIR=$PWD
```

Now, move to the BioBERT code directory. Train the model using:

```bash
mkdir ./tmp/
python3 run_ner.py \
		--do_train=true \
		--do_eval=true \
		--vocab_file=$BIOBERT_DIR/vocab.txt \
		--bert_config_file=$BIOBERT_DIR/bert_config.json \
		--init_checkpoint=$BIOBERT_DIR/model.ckpt-1000000
		--num_train_epochs=10 \
		--data_dir=$NER_DIR \
		--output_dir=./tmp/
```

Presumably, you can then run predictions by setting `--do_train=false –do_predict=true`.

However, BioBERT code seems to keep crashing, complaining about a missing token_test.txt file, for which I raised a [GitHub issue](https://github.com/dmis-lab/biobert/issues/50). Other people also seem to be facing this same issue (for example, see [this issue](https://github.com/dmis-lab/biobert/issues/54)). 

### BioFLAIR

In the meantime, I found another language model called [FLAIR](https://github.com/zalandoresearch/flair/), which has an easy API. There has been an attempt to fine-tune this on PubMed data, called [BioFLAIR](https://github.com/shreyashub/BioFLAIR/). Using FLAIR’s documentation with the data and code from BioFLAIR should be a good alternative to BioBERT.

I was able to use the BioFLAIR code and adapt it to our needs. I trained the model on the `bc5cdr` dataset (provided by the BioFLAIR authors) on a machine with an NVIDIA T4 GPU with 12 GB RAM. Training took 6h 12m. I incorporated training and classification code into the pipeline code.

The trained models are available on [Google Drive](https://drive.google.com/drive/folders/1xfY4k0Sm7Oro4DRepvSyXnhRZnkUkUmd?usp=sharing).

## Current Progress

- [x] **Low confidence text pruning:** Currently achieved by `drugdiscovery.preprocessing.LowConfidencePruner`.
- [x] **Irrelevant term removal:** Currently achieved by `drugdiscovery.preprocessing.IrrelevantTermRemover`.
- [x] **Classification:** Achieved by `drugdiscovery.classification.FlairClassifier`.
- [x] **Adjacent duplicate remover:** Achieved by `drugdiscovery.postprocessing.DuplicateRemover`.
- [x] **Pair formation:** Achieved by `drugdiscovery.postprocessing.PairFormer`.
- [ ] **Validation:** We currently do not have a method for doing this.

The code is available on the [NCSU GitHub](https://github.ncsu.edu/ryedida/drug-disease-predictor) publicly, and the standard [GitHub](https://github.com/yrahul3910/csc830-drug-disease-discovery/) as a private repository shared with Saad.

## Sample run of pipeline

```python
>>> from drugdiscovery.preprocessing import *
>>> from drugdiscovery.postprocessing import *
>>> from drugdiscovery.classification import *
// Some warnings
>>>
>>> pruner = LowConfidencePruner('../../../newJSON')
>>> pruned = pruner.prune()
>>> 
>>> term_remover = IrrelevantTermRemover(pruned)
>>> filtered = term_remover.remove()
>>> 
>>> test = [filtered[4]]
>>> test
["rise blood pressure and blood sugar one of the investigators cardiologist outer Nygard commented the very high intake of total and saturated fat did not increase the calculated risk of cardiovascular diseases or Omeprazole are the most popular treatments for heartburn and reflux disease the FDA consider such so safe that it has approved like Nexium Prevacid and Prilosec for over-the-counter sale but new side effects are still being discovered by researchers and lies medical records of more than $244,000 don't they found that those taking ppis were 19% more likely to experience a stroke over the following six years the higher the dose the greater the risk this was an epidemiological study so cause and effect if not been established the investigator suggest a follow-up clinical"]
>>> classifier = FlairClassifier(save_dir='../../../BioFLAIR/ner/models/v1/')
>>> terms = classifier.classify(test)
2019-12-04 18:16:45,752 loading file ../../../BioFLAIR/ner/models/v1/best-model.pt
>>> 
>>> deduper = DuplicateRemover(terms)
>>> deduped = deduper.remove()
>>> 
>>> pair_former = PairFormer(deduped)
>>> pairs = pair_former.pair()
>>> 
>>> pairs
[('cardiovascular diseases', 'Omeprazole'), ('Omeprazole', 'heartburn'), ('heartburn', 'reflux disease'), ('reflux disease', 'Nexium Prevacid'), ('Nexium Prevacid', 'Prilosec'), ('Prilosec', 'stroke')]
```

## Future Work

* Use metrics to check how well we're doing (validation)
* Check if we could train two models--the first is the one above that finds both, and the second being one that only finds diseases (by training it on a dataset that has diseases rather than just "entities"), and then performing a set difference to get the drugs. We would need to maintain the order somehow and then form adjacent pairs accordingly.

