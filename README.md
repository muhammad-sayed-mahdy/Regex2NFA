# Regex2NFA
Transform regular expression to Non-deterministic Finite Automata (NFA)

## How to run
1. download [graphviz](https://www.graphviz.org/download/) to be able to see the NFA graph.
2. install requirements  
   with pip: `pip install -r requirements.txt`  
   with conda: `conda env create -f environment.yml`, then `conda activate NFA`
3. run `python main.py [-i <input_file>] [-o <ouput_file>]`

   1. input a regex string (e.g. `(a|b)*`) it will produce this image  
      ![image](https://user-images.githubusercontent.com/32793798/118415391-557ec900-b6aa-11eb-9c1c-9a7a0a85b3c3.png)  
      and it will save the JSON file following the [file structure](#output-json-file-structure) of this regex to `output/NFA.json`
   2. if the output file was provided like `python main.py -o output/NFA2`, it will save the json file to `output/NFA2.json`.
   3. if the input file was provided like `python main.py -i ouptut/example.json`, it will output the image corresponding to the input json file  
      ![example](output/example.png)  
      the input json file should follow this [file structure](#output-json-file-structure)

## supported expressions
the valid symbols are alphanumeric or the following special characters
1. `*`: Repetition (0 or more) of the preceding token (e.g. `A*`)
2. `|`: OR between two tokens (e.g. `A|B`)
3. `(` and `)` to group tokens

## Output JSON File Structure
```json
{
    "startingState": "stateA",
    "stateA": {
        "isTerminatingState": false,
        "inputCharacter1": ["stateA"],
        "inputCharacter2": ["stateB", "stateC"]
    },
    "stateB": {
        "isTerminatingState": true,
        "inputCharacter2": ["stateA"]
    },
    "stateC": {
        "isTerminatingState": true,
    }
}
``` 