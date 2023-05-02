# discord ansi 

### Usage
```
py ansi_markdown.py input.dai output.ans 
```

### Syntax
```
(0,5)[1,3,4,9]{
Text here
}
(5,0)[1]{
Another text here
}
(2,3)[9]{
Another Another text here
}
```

### explanation
The syntax is quite simple, there are two digits from 0 to 8 in parentheses, the first digit is foreground, the second background. Numbers stand for colors.

- 0 is black
- 1 is red
- 2 is green
- 3 is yellow
- 4 is blue
- 5 is magenta
- 6 is cyan
- 7 is white
- 8 is default color
Decorators are in square brackets. Their position doesn't matter. They can only be 1, 3, 4, 9

- 1 bold decorator
- 3 italic decorator
- 4 underline decorator
- 9 strikethrough decorator (Doesnt work in discord)
