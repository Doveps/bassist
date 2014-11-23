# Bassist
The bassist reads output produced by the `scanner` and calculates the
baseline for a host, plus modifications made to that host.

# Usage
* Find out where your scanner put its output (for example:
`~/scanner/local`). 
* Find out where your flavor database is (for example: `~/flavors`).

## Comparison
Pass the scanner and flavor directories to the bassist:
`./bassist.py -s ~/scanner/local -f ~/flavors`

## Flavor creation
Pass the scanner and flavor directories to the bassist. Also specify
flavor name:
`./bassist.py -s ~/scanner/local -f ~/flavors -n ubuntu-14.04`

# Setup
Bassist requires Python 2. Other modules include:
- zodb

## OS X
```sh
brew install python3
pip install zodb
```
## Python 2
Why are we using Python 2 and not Python 3? The answer: there is no
working zodb viewer under Python 3 at the moment. Thus, using Python 3
would make development using zodb much more difficult.

# Flavors
If you want to read the flavor database in a friendly format:
* `pip install eye`
* `eye /path/to/flavor.zodb`
* point your web browser at http://localhost:8080

