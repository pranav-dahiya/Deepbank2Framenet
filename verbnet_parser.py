from py4j.java_gateway import JavaGateway


class VerbnetParser:
    """Interface with java Verbnet Parser and provide an entry point from Python"""

    def __init__(self):
        gateway = JavaGateway()
        self.parser = gateway.entry_point.getParser()

    def parse(self, sentence):
        """
        Parse a sentence to get Verbnet predicates

        Args:
            sentence (str): Sentence string

        Returns:
            str: parsed response
        """
        return self.parser.parse(sentence)
