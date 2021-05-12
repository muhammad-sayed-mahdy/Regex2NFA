class InvalidRegex(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Regex2NFA:

    def __init__(self, regex: str) -> None:
        """Initialize NFA builder

        Args:
            regex (str): the regular expression to transform into NFA
        """
        self.text = regex
        self.validate()
        self.nfa = {}
        

    def process(self):
        """transform the regex string into NFA dictionary
        """
        pass

    def validate(self):
        """validate the input regex string

        Raises:
            Exception: [description]
            Exception: [description]
            Exception: [description]
            Exception: [description]
            Exception: [description]
            Exception: [description]
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
            
    