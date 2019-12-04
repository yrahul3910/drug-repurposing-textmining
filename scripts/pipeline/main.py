from drugdiscovery.preprocessing import LowConfidencePruner, IrrelevantTermRemover
from drugdiscovery.postprocessing import DuplicateRemover, PairFormer
from drugdiscovery.classification import FlairClassifier

print('(1 / 5) Pruning low confidence excerpts')
pruner = LowConfidencePruner('../../Transcripts/newJSON')
pruned = pruner.prune()

print('(2 / 5) Removing irrelevant terms')
term_remover = IrrelevantTermRemover(pruned)
filtered = term_remover.remove()

print('(3 / 5) Classifying')
classifier = FlairClassifier()
medical_term_strings = classifier.classify(filtered)

print('(4 / 5) Removing duplicates')
deduper = DuplicateRemover(medical_term_strings)
deduped = deduper.remove()

print('(5 / 5) Forming pairs')
pair_former = PairFormer(deduped)
pairs = pair_former.pair()

print(pairs)
