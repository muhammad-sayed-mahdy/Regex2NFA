from Regex2NFA import InvalidRegex, Regex2NFA
import argparse

outputFile = "output/NFA"
parser = argparse.ArgumentParser()
parser.add_argument('-i', "--iFile", help="input file")
parser.add_argument('-o', "--oFile", help="output file")
args = parser.parse_args()

inputFile = args.iFile
if args.oFile:
    outputFile = args.oFile

if inputFile:
    nfa = Regex2NFA()
    nfa.loadFromFile(inputFile)
    nfa.toGraph(outputFile)

else:
    while True:
        try:
            s = input("Enter the regex string\n")
            nfa = Regex2NFA(s)
            nfa.process()
            nfa.saveToFile(outputFile)
            nfa.toGraph(outputFile)

            break
        except InvalidRegex as e:
            print(e)
