from dom_tree import Node

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
                attr[curr_key.lstrip()] = string[lagging_pointer + 1: pointer]

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
                #add text node to parent
                text_node = Node("text")
                text_node.attributes["text"] = html[lagging_pointer + 1: pointer]
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
                node = Node(html[lagging_pointer + 1: pointer].replace("/", ""))
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
    return stack[0].nodes[0]