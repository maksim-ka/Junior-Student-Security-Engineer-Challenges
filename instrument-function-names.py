#!/usr/bin/env python3
# coding: utf-8

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs=1, help='Input file name.')
parser.add_argument('output', nargs=1, help='Outpu file name.')
args = parser.parse_args()

in_filename = args.input[0]
out_filename = args.output[0]

import re
# func main() {
re_func=re.compile(r"^func (.*)\(.*\) *\{$")
# bar()
re_call=re.compile(r"^\s*([^\.]*)\(.*\)")

def parse(line,re):
    m = re.search(line)
    if m is None:
        return None
    else:
        return m.group(1)

   
DEBUG =0
#DEBUG=1
#DEBUG=2

with open(out_filename,'w') as output, open(in_filename) as input :
  re=re_func
  for line in input: 
    output.write(line)
    p=parse(line,re)
    
    if DEBUG > 0:
      print("## looking for ",end='')
      if re is re_func:
        print("func")
      if re is re_call:
        print("call")
      
      print(line,end='')
    
    if re == re_func and p != None:
      #cg=CallGraph(p, [])
      func = p
      calls = []
      
      output.write(f"\tfmt.Println(\"{p}\")\n")

      if DEBUG >0: print(f"## we found the func: {p}")
      #if DEBUG >1: print(f"#### cg: {cg}")
      re=re_call #next look for calls

    elif re == re_call and line.strip() == "}":
      #dict_CallGraph[cg.func]=cg.calls

      if DEBUG >0: print(f"## func {func} has ended")
      #if DEBUG >1: print(f"#### cg: {cg}")

      re=re_func  #look for func again    

    elif re == re_call and p != None:   
      calls.append(p)

      if DEBUG >0: print(f"## we found a func call: {p}()")
      #if DEBUG >1: print(f"#### cg: {cg}")

    if DEBUG >0: print()


