from .dom_tree import Node

def parse_attributes(string):
    attr = {}
    curr_key = ""

    lagging_pointer = 0
    pointer = 0

    val = False

    for c in string:
        if c == '"':
            if not val: 
                val = True
            else:
                val = False
                attr[curr_key.strip()] = string[lagging_pointer + 1: pointer]

            lagging_pointer = pointer
        if c == '=':
            curr_key = string[lagging_pointer + 1: pointer]

        pointer += 1
    return attr

def parse(html):
    #list for self closing tags
    self_closing = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]
    #stack for nodes
    stack = []
    #states:
    #0 - traversing
    #1 - tag detected
    #2 - reading attributes
    #3 - ignoring
    #4 - closing tag detected
    state = 0
    #pointers
    pointer = 0
    lagging_pointer = 0

    #create root node
    stack.append(Node("ROOT"))
    #parser loop
    for c in html:
        if state == 0:
            if c == '<':
                #add text node to parent and check if it is only whitespace
                text = html[lagging_pointer + 1: pointer].strip()
                if text:
                    text_node = Node("text")
                    text_node.attributes["text"] = text
                    stack[-1].add_node(text_node)

                lagging_pointer = pointer
                state = 1
            pointer += 1

        elif state == 1:
            #set ignore if comment
            if c == '!':
                state = 3
            if c == '/' and html[pointer-1] == '<':
                state = 4
            if c == ' ' or c == '>':
                #create node and add to parent and push on stack
                node = Node(html[lagging_pointer + 1: pointer].replace("/", "").lower())
                stack[-1].add_node(node)
                stack.append(node)

                lagging_pointer = pointer
                state = 2 if c == ' ' else 0

                #remove node from stack if self closing and no attributes are to assign
                if node.tag in self_closing and state != 2: stack.pop()

            pointer += 1

        elif state == 2:
            if c == ">":
                #update attributes
                stack[-1].attributes.update(parse_attributes(html[lagging_pointer: pointer]))

                lagging_pointer = pointer
                state = 0
                #remove node from stack if element is self closing
                if stack[-1].tag in self_closing: stack.pop()

            pointer += 1

        elif state == 3:
            if c == '>':
                #checks if comment
                #ignores also <!Doctype html>
                if html[lagging_pointer: lagging_pointer + 4] == "<!--":
                    if html[pointer - 2: pointer] == "--":
                        state = 0
                        lagging_pointer = pointer
                else:
                    state = 0
                    lagging_pointer = pointer

            pointer += 1
        
        elif state == 4:
            #remove last element from stack
            if c == '>':
                stack.pop()
                state = 0
                lagging_pointer = pointer

            pointer +=1
    return list(filter(lambda x: x.tag == "html", stack[0].nodes))[0]

#how the parser works:
#
#We have a stack to keep track which element we are in currently
#e.g.
#
#<div>
#   <p>
#       ...inside a paragraph...
#   </p>
#</div>
#
#We have two pointers (lagging pointer and pointer) to slice parts of the html string
#e.g.   ()... is the pointer position
#
#<p(>)Example Text(<)/P>        we can use html[lagging_pointer + 1: pointer] to get the text inside the <p> element
#
#the pointer points to the current character, while the lagging pointer only changes when states change
#
#There are five states:
#0 - Traversing:
#   -is active when we are outside a tag
#   -as soon as a tag is detected we switch to state 1
#   -we create a text node with the text between the two pointers and add it to the node on top of the stack
#   -lagging pointer is set to the current character which is the opening bracket "<"
#
#1 - Tag detected:
#   -First we need to find out what type of tag we have:
#       -if the next character is a "!" we know it is a comment so we switch to state 3
#       -if the next character is a "/" we know it is a closing tag so we switch to state 4
#       -unless one of the conditions is true we know it is an opening tag
#   -if we have an opening tag:
#       -we continue until either a space or an ">" is met
#       -then we will create a new Node with the tag being the text between the two pointers
#       -the new node will be pushed onto the stack
#       -if the current character is ">" we switch back to state 0
#       -otherwise we switch to state 2
#       -lagging pointer is moved to current character
#       -if we switched to state 0, we have to check if the element we added to the stack is self closing (e.g. <input>, <img>)
#       -if yes we remove it
#
#2 - Reading attributes:
#   -we continue until a ">" is met
#   -we pass the string containing all attributes (using the pointers) to another parsing function
#   -the function returns a dictionary with all attributes that we add to the node on top of the stack
#   -if the node on top of the stack is self closing, remove it
#   -we switch back to state 0 and set the lagging pointer to the current character
#
#3 - ignoring:
#   -simply continues until end of comment is found
#   -lagging pointer is set to current character position
#   -we switch to state 0
#
#4 - Closing tag detected:
#   -we continue until end of tag is found (">")
#   -we pop last element from stack
#   -move lagging pointer to current character position
#   -switch to state 0
