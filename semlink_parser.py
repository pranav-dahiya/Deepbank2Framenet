import re
import os.path
from typing import TextIO

from constants import SEMLINK_FILE
from data_classes import SemlinkInstance
from propbank_parser import PropbankParser


def class_map(x):
    return x if x != 'None' else 'NF'


class SemlinkParser:
    """Class for parsing Semlink file"""
    file_path = None
    parser = PropbankParser()

    def __init__(self, file_path=SEMLINK_FILE):
        """
        init method for the class

        Args:
            file_path (str): path to semlink file
        """
        self.file_path = file_path

    def __parse_line_v13(self, line):
        """
        Parse one line from semlink file

        Args:
            line (str): Semlinke file line

        Returns:
            SemlinkInstance: parsed information
        """
        elems = line.split()
        if '.mrg' in elems[0]:
            return
        sentence_id = int('2' + re.search(r'\d+', os.path.basename(elems[0])).group()) * 1000 + int(elems[1]) + 1
        token = self.parser.get_token(elems[0], int(elems[1]), int(elems[2]))
        args = re.findall(r'ARG\d=\w+;\w+', line)
        args = [arg.split('=') for arg in args]
        args = {arg[0]: arg[1].split(';')[1] for arg in args}
        return SemlinkInstance(sentence_id, token, elems[3], class_map(elems[5]), args)

    def __parse_line_v122(self, line):
        """
        Parse one line from semlink file

        Args:
            line (str): Semlinke file line

        Returns:
            SemlinkInstance: parsed information
        """
        elems = line.split()
        if '.mrg' in elems[0]:
            return
        sentence_id = int('2' + re.search(r'\d+', os.path.basename(elems[0])).group()) * 1000 + int(elems[1]) + 1
        token = self.parser.get_token(os.path.basename(elems[0]), int(elems[1]), int(elems[2]))
        args = re.findall(r'ARG\d=\w+;\w+', line)
        args = [arg.split('=') for arg in args]
        args = {arg[0]: arg[1].split(';')[1] for arg in args}
        return SemlinkInstance(sentence_id, token, elems[4], class_map(elems[6]), args)

    def parse_line(self, line):
        if '1.3' in self.file_path:
            return self.__parse_line_v13(line)
        elif '1.2.2' in self.file_path:
            return self.__parse_line_v122(line)
        else:
            raise Exception(f'{self.file_path} is not a recognized semlink file')

    def parse_file(self):
        """
        Parses entire semlink file and returns a list

        Returns:
            list[SemlinkInstance]: list of semlink instances
        """
        with open(self.file_path) as f:
            return [self.parse_line(line) for line in f.readlines()]


if __name__ == '__main__':
    import pickle

    parser = SemlinkParser()
    semlink = parser.parse_file()
    semlink = [instance for instance in semlink if instance and instance.frame not in ('IN', 'NF')]
    with open('semlink.pickle', 'wb+') as f:
        pickle.dump(semlink, f)
