# TreepyParser

TreepyParser is a python library that parses html into a tree structure

## Installation

Use the following command to install

```bash
pip install TreepyParser
```

## How to use
```python
import TreepyParser

#pass string containing html
parser.parse(html) #returns html tree
```
The tree returned is a node representing the <html> element that contains all other elements

Nodes have following methods and variables 
```python
node.tag #string representing element e.g. div, p, table
node.get_attribute(key) #returns attribute value, e.g. href => www.example.com
node.add_node(n) #adds node n to node
node.insert_node(n, pos) #inserts node n at position pos of node, previous node at pos will be a child of node n
node.remove_node(pos, remove_subtree) #removes node at pos, if remove_subtree is false children of the removed node will be added to node
node.find(tag="", **kwargs) #returns list of all matches in subtree, kwargs represent attributes
```

## License
MIT