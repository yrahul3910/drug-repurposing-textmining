from drugdiscovery.preprocessing import LowConfidencePruner, IrrelevantTermRemover
from drugdiscovery.postprocessing import DuplicateRemover, PairFormer
from drugdiscovery.classification import FlairClassifier

pruner = LowConfidencePruner('../../Transcripts/newJSON')
pruned = pruner.prune()

term_remover = IrrelevantTermRemover(pruned)
filtered = term_remover.remove()

classifier = FlairClassifier()
medical_term_strings = classifier.predict(filtered)

deduper = DuplicateRemover(medical_term_strings)
deduped = deduper.remove()

pair_former = PairFormer(deduped)
pairs = pair_former.pair()

print(pairs)
