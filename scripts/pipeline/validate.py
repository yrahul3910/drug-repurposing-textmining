"""
Assuming main.py was run as described.
"""
import sys
import json
from drugdiscovery.validation import RobokopValidator

if len(sys.argv) != 2:
    print('Usage: python3 validate.py INPUT')
    exit(1)

# need to read in password, get pairs, and pass to the validator.
with open('.password', 'r') as f:
    password = f.read()[:-1]

print(password)

with open(sys.argv[1], 'r') as f:
    pairs = json.load(f)

validator = RobokopValidator(pairs, password=password)
validator.validate()
