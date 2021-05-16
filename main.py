from Regex2NFA import InvalidRegex, Regex2NFA
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
    nfa = Regex2NFA()
    nfa.loadFromFile(filename)
    nfa.toGraph()
    
else:
    while True:
        try:
            s = input("Enter the regex string\n")
            nfa = Regex2NFA(s)
            nfa.process()
            nfa.saveToFile("output/NFA.json")
            nfa.toGraph()

            break
        except InvalidRegex as e:
            print(e)
