import os
import re
from constants import PROPBANK_PATH


class PropbankParser:
    path = None

    def __init__(self, path=PROPBANK_PATH):
        self.path = path

    def get_token(self, filename, sentence, token):
        with open(os.path.join(self.path, filename)) as f:
            file_contents = f.read()
            tree = file_contents.split('\n\n')[sentence]
        tokens = [re.search(r'(?<=\()[^()]+(?=\))', line).group().split()[-1] for line in tree.splitlines()]
        return tokens[token]
