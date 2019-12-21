# Parsing the output
To get the `test-pairs` file from the various output files, first run in a shell:

```{sh}
for file in $(ls -v *.txt); do egrep "^\[.+\]" $file > pairs; done
tr "\n" "," < pairs > pairs_ && rm pairs
tr "(" "[" < pairs_ > pairs && rm pairs_
tr ")" "]" < pairs > pairs_ && rm pairs
```

Then open an interactive Python shell and type:

```{py}
import ast
import json

with open('pairs_', 'r') as f:
    line = f.read()[:-1]  # Gets rid of trailing comma

nested = ast.literal_eval(line)
pairs = [item for sublist in nested for item in sublist]

with open('test-pairs', 'w') as f:
    json.dump(pairs, f)
```
