from graphviz import Digraph
import json

class InvalidRegex(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidNFA(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Regex2NFA:

    def __init__(self, regex: str = None) -> None:
        """Initialize NFA builder

        Args:
            regex (str): the regular expression to transform into NFA
        """
        self.text = regex
        self.nfa = {}

    def process(self):
        """transform the regex string into NFA dictionary
        """
        self.validate()

    def validate(self) -> None:
        """validate the input regex string

        Raises:
            InvalidRegex: if the regex string is invalid
        """
        specialChars = {'*', '|', '(', ')'}

        if len(self.text) == 0:
            raise InvalidRegex("Input regex cannot be empty")

        for i,c in enumerate(self.text):
            if not(c.isalnum() or c in specialChars):
                raise InvalidRegex(f"{c} is not supported symbol")
            if (c == '*' or c == '|') and (i == 0 or self.text[i-1] == '*' or self.text[i-1] == '|' or self.text[i-1] == '('):
                raise InvalidRegex(f"Invalid usage of '{c}'")
        
        # verify opening and closing brackets
        openBrackets = 0
        for c in self.text:
            if (c == '('):
                openBrackets += 1
            elif (c == ')'):
                if openBrackets == 0:
                    raise InvalidRegex("Unmatched closing bracket")
                openBrackets -= 1
        if openBrackets != 0:
            raise InvalidRegex("Unmatched opening bracket")

        if self.text[-1] == '|':
            raise InvalidRegex("Invalid usage of '|'")

    def loadFromFile(self, filename: str):
        """Load NFA from a json file

        Args:
            filename (str): file name
        """
        with open(filename, 'r') as f:
            self.nfa = json.load(f)

        self.validateNFA()

    def saveToFile(self, filename: str):
        """save the NFA to a json file

        Args:
            filename (str): file name
        """
        with open(filename, "w") as f:
            json.dump(self.nfa, f)

    def validateNFA(self):
        """check if the NFA is valid

        Raises:
            Exception: if the NFA is invalid
        """
        if "startingState" not in self.nfa:
            raise Exception("invalid NFA")

        for k, v in self.nfa.items():
            if k != "startingState" and ("isTerminatingState" not in v):
                raise Exception("invalid NFA")

    def toGraph(self):
        """transform the NFA dictionary into graph and visualize it
        """
        self.validateNFA()
        terminating = []
        starting = self.nfa["startingState"]
        del self.nfa['startingState']
        for k, v in self.nfa.items():
            if v['isTerminatingState']:
                terminating.append(k)
            del v['isTerminatingState']

        g = Digraph("NFA", filename="output/NFA.gv", format='png')
        g.attr('node', shape='doublecircle')
        for node in terminating:
            g.node(node)
        
        g.attr('node', shape='circle')
        g.node(starting)
        for u, children in self.nfa.items():
            for e, v in children.items():
                g.edge(u, v, label=e)

        g.attr('node', shape='plaintext')
        g.node('starting', label='')
        g.edge('starting', starting)

        g.view()
    