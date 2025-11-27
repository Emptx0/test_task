import re

FORBIDDEN_RE = re.compile(r'[!@#$%^&*()\[\]{};:\'\"<>,./?~\\|+\-=]')

word = "asd5$"

print(bool(FORBIDDEN_RE.search(word)))