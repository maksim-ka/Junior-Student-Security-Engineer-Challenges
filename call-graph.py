#!/usr/bin/env python3
# coding: utf-8

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs=1, help='Input file name.')
args = parser.parse_args()

filename = args.input[0]

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

   
dict_CallGraph={}
DEBUG =0

with open(filename) as input:
  re=re_func
  for line in input: 
    p=parse(line,re)
    
    if DEBUG > 0:
      print("## looking for ",end='')
      if re is re_func:
        print("func")
      if re is re_call:
        print("call")
      
      print(line,end='')
    
    if re == re_func and p != None:
      func = p
      calls = []
      

      if DEBUG >0: print(f"## we found the func: {p}")
      if DEBUG >1: print(f"#### cg: {cg}")

      re=re_call #next look for calls

    elif re == re_call and line.strip() == "}":
      dict_CallGraph[func]=calls

      if DEBUG >0: print(f"## func {cg.func} has ended")
      if DEBUG >1: print(f"#### cg: {cg}")

      re=re_func  #look for func again    

    elif re == re_call and p != None:   
      calls.append(p)

      if DEBUG >0: print(f"## we found a func call: {p}()")
      if DEBUG >1: print(f"#### cg: {cg}")

    if DEBUG >0: print()

DEBUG =0
maxFuncName=5
def traverse (graph,source,visited):
    if DEBUG>0: print (' <{}|{}|{}>'.format(len(graph),len(visited),visited), end = '')
    if source in visited:
        if DEBUG>0: print (" cycle!", end = '')
        for i in visited:
                print("{}-->".format(i),end='')
        print (("{}".format(source)).ljust(maxFuncName))
        #print()
        #visited.remove(source)
        return
    visited.append (source)
    if DEBUG >2: print ("(:{})".format(graph[source]), end = '')
    i=0
    for node in graph[source]:
        if len(graph[node]) > 0:
            traverse (graph, node, visited)
        else:
            if DEBUG>0: print (' <{}|{}|{}>'.format(len(graph),len(visited),visited), end = '')
            for i in visited:
                print("{}-->".format(i),end='')
            print ("{} ".format(node))
            return
        i+=1
    visited.remove(source)
    return

traverse(dict_CallGraph,'main',list())
