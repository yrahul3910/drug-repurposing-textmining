from drugdiscovery.preprocessing import LowConfidencePruner, IrrelevantTermRemover
from drugdiscovery.postprocessing import DuplicateRemover, PairFormer
from drugdiscovery.classification import FlairClassifier

print('(1 / 5) Pruning low confidence excerpts')
pruner = LowConfidencePruner('../../../Transcripts/newJSON')
pruned = pruner.prune()

print('(2 / 5) Removing irrelevant terms')
term_remover = IrrelevantTermRemover(pruned)
filtered = term_remover.remove()

print('(3 / 5) Classifying')
classifier = FlairClassifier(save_dir='../../../')
# classifier.train()

print('Classifying', len(filtered), 'terms')

batch_size = 16
for i in range(0, len(filtered), batch_size):
    print('\n\n....Batch', i // batch_size + 1, '/', len(filtered) // batch_size, '\n------------------')
    medical_term_strings = classifier.classify(filtered[i:i+batch_size])

    with open('terms.txt', 'a') as f:
        if len(medical_term_strings) > 0:
            f.write(str(medical_term_strings))

    deduper = DuplicateRemover(medical_term_strings)
    deduped = deduper.remove()

    pair_former = PairFormer(deduped)
    pairs = pair_former.pair()

    print(pairs)
