# Regex2NFA
Transform regular expression to Non-deterministic Finite Automata (NFA)

## How to run
1. download [graphviz](https://www.graphviz.org/download/) to be able to see the NFA graph.
2. install requirements by running  
   `pip install -r requirements.txt`

## supported expressions
the valid symbols are alphanumeric or the following special characters
1. '\*': Repetition (0 or more) of the preceding token (e.g. A\*)
2. '|': OR between two tokens (e.g. A|B)
3. '(' and ')' to group tokens
