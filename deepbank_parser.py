import os.path
import re
from ast import literal_eval
from delphin.codecs import eds
from constants import DEEPBANK_PATH
from data_classes import DeepbankSentence


class DeepbankParser:
    """Parse deepbank files to collect eds graph"""
    path = None

    def __init__(self, path=DEEPBANK_PATH):
        """
        init method of the class

        Args:
            path (str): path to Deepbank directory
        """
        self.path = path

    def parse_sentence(self, filename):
        """
        Read and parse a sentence in a Deepbank file

        Args:
            filename (str): relative path to file from Deepbank directory

        Returns:
            DeepbankSentence: Parsed sentence
        """
        filename = str(filename)
        try:
            with open(os.path.join(self.path, filename)) as f:
                data = f.read().split('\n\n')
        except FileNotFoundError:
            return
        sentence = data[1][data[1].index('`')+1: data[1].index("'")]
        tokens = data[2].split('\n')[1:-1]
        token_lnks = [re.search(r'<.*>', token).group() for token in tokens]
        tokens = [re.sub(r', <.*>', '', token).strip() for token in tokens]
        tokens = [(literal_eval(re.sub(r'(?<!,) ', ', ', token))[4], lnk) for token, lnk in zip(tokens, token_lnks)]
        try:
            eds_tree = eds.decode(re.sub(r',(?=.*nn_u_unknown)', '', data[7]))
        except Exception as e:
            print(filename)
            print(data[7])
            print(e)
            return
        return DeepbankSentence(int(os.path.basename(filename)), sentence, tokens, eds_tree)


if __name__ == '__main__':
    import pickle
    parser = DeepbankParser()
    with open('semlink.pickle', 'rb') as f:
        semlink = pickle.load(f)
    id_set = set([instance.id for instance in semlink if instance])
    deepbank = [parser.parse_sentence(val) for val in id_set]
    with open('deepbank.pickle', 'wb+') as f:
        pickle.dump(deepbank, f)
