import sys

start = "\x1b[{};{};{}m"

end = "\x1b[0m\n"
lastlist= 0
foreground = {
    "black":30,
    "red":31,
    "green":32,
    "yellow":33,
    "blue":34,
    "magenta":35,
    "cyan":36,
    "white":37,
    "default":39 
}
backgroud = {
    "black":40,
    "red":41,
    "green":42,
    "yellow":43,
    "blue":44,
    "magenta":45,
    "cyan":46,
    "white":47,
    "default":49
}
style = {
    "bold":1,
    "italic":3,
    "underline":4,
    "strikethrough":9
}




elements = {
    "title": lambda text: start.format(37,49,1) + text + "\n" + "-"*len(text)+ "\n",
    "subtitle":lambda text: start.format(37,49,1) + text
    }



file = open(sys.argv[1],'r',encoding='utf-8').readlines()
#print(file)

class parser:
    result = []
    tree = []
    tokens = {
        "title":'[[title]]',
        "subtitle":"[[subtitle]]",
        "end":"[[end]]",
        "list":"[[list]]",
        "el":"[[el]]",
        }
    def mark(self):
        global file, lastlist
        for line in file:
            if line.find("[[subtitle]]") >= 0:

                line = line.removeprefix("[[subtitle]]")

                s,e = line.find('['), line.find(']')

                if s >= 0 and e >= 0:
                    self.result.append(self.subtitle(line[s+1:e]))
                else:
                    print('syntax error')
                    break
            elif line.find("[[title]]") >= 0:

                line = line.removeprefix("[[title]]")

                s,e = line.find('['), line.find(']')

                if s >= 0 and e >= 0:
                    self.result.append(self.title(line[s+1:e]))
                else:
                    print('syntax error')
                    break       
            elif line.find("[[list]]") >= 0:

                line = line.removeprefix("[[list]]")

                s,e = line.find('['), line.find(']')

                if s >= 0 and e >= 0:
                    lastlist = len(line[s+1:e])
                    self.result.append(self.listtitle(line[s+1:e]))
                else:
                    print('syntax error')
                    break
            elif line.find("[[el]]") >= 0:

                line = line.removeprefix("[[el]]")

                s,e = line.find('['), line.find(']')

                if s >= 0 and e >= 0:
                    self.result.append(self.listel(line[s+1:e]))
                else:
                    print('syntax error')
                    break
            elif line.find("[[listend]]") >= 0:

                line = line.removeprefix("[[list]]")

                s,e = line.find('['), line.find(']')

                if s >= 0 and e >= 0:
                    self.result.append(self.listend(lastlist))
                else:
                    print('syntax error')
                    break
            
                
            elif line.find("[[colorline(") >= 0:
                
                line = line.removeprefix("[[colorline")
                x,y = line.find("("), line.find(")")
                d = line[x+1:y].split(',')
                line = line.removeprefix(line[x:y+3])
                s,e = line.find('['), line.find(']')

                if s >= 0 and e >= 0:
                    self.result.append(self.colorline(line[s+1:e],*d))
                else:
                    print('syntax error')
                    break
            else:
                self.result.append(line)






    def colorline(self,text,fg,bg):
        return start.format(foreground[fg],backgroud[bg],2) + text + end

    def title(self, text):
        return start.format(37,49,1) + text + "\n" + "-"*len(text) + end

    def subtitle(self,text):
        return start.format(37,49,"1;4") + text + end

    def listtitle(self,text):
        return start.format(37,49,0) + text + "\n" + "="*len(text) + end

    def listend(self,x):
        return start.format(37,49,0) + "="*x + end

    def listel(self,text):
        return start.format(37,49,0) + "  ‣" + text + end

    def end(self):
        return end
    


x = parser()

x.mark()
print(x.result)
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    for line in x.result:
        f.write(line)