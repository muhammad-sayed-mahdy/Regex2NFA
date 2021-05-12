from Regex2NFA import InvalidRegex, Regex2NFA

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
