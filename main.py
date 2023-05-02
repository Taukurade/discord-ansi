import sys
import argparse
from dotmap import DotMap as Map


class Parser:
    def __init__(self,input:str,output:str,wrap:bool) -> None:
        self.tree = Map(root=[])
        print("reading...")
        self.code = open(input,'r').read()
        self.wrap = wrap
        self.pos = 0
        self.iter_pos = 0
        self.output = open(output,'w')
        self.tokens = []
        self.reset = "\x1b[0m"


    def proceed(self):
        print("parsing...")
        self.parse()
        print("generating AST tree...")
        self.gen_tree()
        print("proceeding with output...")
        self.out()
        print("done :3")

    def parse(self):
        for i in self.code:
            if self.pos < self.iter_pos:
                self.pos += 1
                continue
            if i == "(" or i == ")":
                self.tokens.append(i)
            if i == "[" or i == "]":
                self.tokens.append(i)
            if i.isdigit():
                self.tokens.append(int(i))
            
            if i == "{":
                self.tokens.append(i)
                s,e = self.pos+1,self.pos    
                for d in self.code[self.pos:]:
                    if d == "}":
                        self.iter_pos = e
                        self.tokens.append(self.code[s:e])
                        self.tokens.append(d)
                        
                        break
                    
                    e+=1
            
            self.pos +=1

    def gen_tree(self):
        self.pos = 0
        cur_DC = 0
        cur_TX = 0
        for token in self.tokens:
            
            if token == "(":
                
                self.tree['root'].append(Map(FG=self.tokens[self.pos+1],BG=self.tokens[self.pos+2],DC=[],text=""))
            if token == "[":
                self.tree.root[cur_DC].DC = self.tokens[self.pos+1:self.tokens.index("]",self.pos)]
                cur_DC += 1
            if token == "{":
                self.tree.root[cur_TX].text = self.tokens[self.pos+1]
                cur_TX += 1
            self.pos += 1

    def out(self):
        result = ""
        for block in self.tree.root:
            result += f"\x1b[{30+block.FG};{40+block.BG}m" + self.decorate(block.DC) + block.text + self.reset
        if self.wrap: result = f"```ansi\n {result}\n```"
        self.output.write(result)
        self.output.close()

    def decorate(self,decs):
        decs = [str(i) for i in decs]
        if len(decs) > 0:return f"\x1b[{';'.join(decs)}m"
        return ""


def main():
    argprs = argparse.ArgumentParser(
                    prog='Discord ansi',
                    description='convert simple-to-undestand syntax to escape sequence decorated text')
    argprs.add_argument('input',help="input filename, can be /dev/stdin (linux only) to direct input. tap ctrl+D to end input")
    argprs.add_argument('output',help="output filename, can be /dev/stdout (linux only) to output directly in terminal")
    argprs.add_argument('-w','--wrap',action='store_true',help="wraps result in discord code snippet")
    args = argprs.parse_args()
    parser = Parser(args.input,args.output,args.wrap)
    parser.proceed()
main()