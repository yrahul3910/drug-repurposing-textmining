"""
Assuming main.py was run as described.
"""
import json
from drugdiscovery.validation import RobokopValidator

# need to read in password, get pairs, and pass to the validator.
with open('.password', 'r') as f:
    password = f.read()

with open('output.txt', 'r') as f:
    pairs = json.load(f)

validator = RobokopValidator(pairs)
validator.validate()
