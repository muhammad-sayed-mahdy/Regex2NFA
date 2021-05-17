from graphviz import Digraph
import json

class InvalidRegex(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidNFA(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

SPECIAL_CHARS = {'*', '|', '(', ')'}
EPS = 'ϵ'
class Regex2NFA:

    def __init__(self, regex: str = None) -> None:
        """Initialize NFA builder

        Args:
            regex (str): the regular expression to transform into NFA
        """
        self.text = regex
        self.nfa = {}
        self.statesCount = 0


    def validate(self) -> None:
        """validate the input regex string

        Raises:
            InvalidRegex: if the regex string is invalid
        """
        

        if len(self.text) == 0:
            raise InvalidRegex("Input regex cannot be empty")

        for i,c in enumerate(self.text):
            if not(c.isalnum() or c in SPECIAL_CHARS):
                raise InvalidRegex(f"'{c}' is not a supported symbol")
            if c == '*' and (i == 0 or self.text[i-1] == '*' or self.text[i-1] == '|' or self.text[i-1] == '('):
                raise InvalidRegex(f"Invalid usage of '*'")
            elif c == '|' and (i == 0 or self.text[i-1] == '|' or self.text[i-1] == '('):
                raise InvalidRegex(f"Invalid usage of '|'")
            elif (c == ')') and (i == 0 or self.text[i-1] == '|'):
                raise InvalidRegex(f"Invalid usage of ')'")
            
        
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

    def __addState(self):
        self.nfa[str(self.statesCount)] = {}
        self.nfa[str(self.statesCount)]['isTerminatingState'] = False
        self.statesCount += 1
        return str(self.statesCount-1)

    def __addNFA(self,u,v,event):
        self.nfa[u][v] = event

    def __groupingStage(self, text):
        events = []
        i = 0
        while i < len(text):
            event = {}
            if text[i] == '(':
                j = i
                brackets = 1
                while brackets > 0: 
                    j += 1
                    if text[j] == ')':
                        brackets -= 1
                    if text[j] == '(':
                        brackets += 1
                newExp = text[i+1:j]
                event = self.__solve(newExp)
                events.append(event)
                i = j
            if text[i].isalnum():
                event["type"] = "exp"
                event["start"] = self.__addState()
                event["end"] = self.__addState()
                self.__addNFA(event["start"], event["end"], text[i])
                events.append(event)
            if text[i] == '*':
                event["type"] = "rep"
                events.append(event)
            if text[i] == '|':
                event["type"] = "or"
                events.append(event)
            i += 1
        return events

    def __repeatStage(self, grevents):
        i = 1
        events = []
        while i <= len(grevents):
            event = grevents[i-1]
            if i < len(grevents) and grevents[i]["type"] == 'rep':
                st = self.__addState()
                en = self.__addState()
                self.__addNFA(st,event["start"], EPS)
                self.__addNFA(event["end"], st, EPS)
                self.__addNFA(event["end"], en, EPS)
                self.__addNFA(st, en, EPS)
                event["start"] = st
                event["end"] = en
                events.append(event)
                i += 1
            else:
                events.append(event)
            i += 1
        return events

    def __concatenateStage(self, rpevents):
        i = 1
        events = []
        while i < len(rpevents):
            event = rpevents[i-1]
            if rpevents[i]["type"] == "or":
                events.append(event)
                i += 2
            else:
                event["start"] = rpevents[i-1]["start"]
                while i < len(rpevents) and rpevents[i]["type"] != "or":
                    self.__addNFA(rpevents[i-1]["end"], rpevents[i]["start"], EPS)
                    event["end"] = rpevents[i]["end"]
                    i += 1
                events.append(event)
                i += 2
        if i == len(rpevents):
            events.append(rpevents[i-1])
        return events

    def __orStage(self, concevents):
        e = {}
        if len(concevents) == 1:
            return concevents[0]
        e["start"] = self.__addState()
        e["end"] = self.__addState()
        e["type"] = "exp"
        for i in concevents:
            self.__addNFA(e["start"], i["start"],EPS)
            self.__addNFA(i["end"], e["end"],EPS)
        return e

    def __solve(self, text):
        # 1- grouping
        grevents = self.__groupingStage(text)
        # 2- repeatition
        rpevents = self.__repeatStage(grevents)
        # 3- Concatenation
        concevents = self.__concatenateStage(rpevents)
        # 4- Oring
        return self.__orStage(concevents)
                


        

    def process(self):
        """transform the regex string into NFA dictionary
        """
        self.validate()
        e = self.__solve(self.text)
        self.nfa[e["end"]]['isTerminatingState'] = True
        for k, v in self.nfa.items():
            node = {}
            for a, b in v.items():
                if a == "isTerminatingState":
                    node[a] = b
                    continue
                if not (b in node):
                    node[b] = []
                node[b].append(a)
            self.nfa[k] = node
        self.nfa["startingState"] = e["start"]
        
        
    def loadFromFile(self, filename: str):
        """Load NFA from a json file

        Args:
            filename (str): file name
        """
        with open(filename, 'r') as f:
            self.nfa = json.load(f)


    def saveToFile(self, filename: str):
        """save the NFA to a json file

        Args:
            filename (str): file name
        """
        filename += ".json"
        with open(filename, "w") as f:
            json.dump(self.nfa, f)

    def validateNFA(self):
        """check if the NFA is valid

        Raises:
            InvalidNFA: if the NFA is invalid
        """
        if "startingState" not in self.nfa:
            raise InvalidNFA()

        for k, v in self.nfa.items():
            if k != "startingState" and ("isTerminatingState" not in v):
                raise InvalidNFA()

    def toGraph(self, filename):
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

        filename += ".gv"
        g = Digraph("NFA", filename=filename, format='png')
        g.attr('graph', rankdir='LR')
        g.attr('node', shape='doublecircle')
        for node in terminating:
            g.node(node)
        
        g.attr('node', shape='circle')
        g.node(starting)
        for u, children in self.nfa.items():
            for e, arr in children.items():
                for v in arr:
                    g.edge(u, v, label=e)

        g.attr('node', shape='plaintext')
        g.node('starting', label='')
        g.edge('starting', starting)

        g.view()
    