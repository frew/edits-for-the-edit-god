import json
import sys
import types
from pprint import pprint
from xml import sax

def addElem(subelemStack, holder, content):
  for attribute in subelemStack[:-1]:
    holder.setdefault(attribute, {})
    if not isinstance(holder[attribute], dict):
      holder[attribute] = {}
    holder = holder[attribute]

  holder.setdefault(subelemStack[-1], '')
  if not (subelemStack[-1] in holder and isinstance(holder[subelemStack[-1]], dict)):
    holder[subelemStack[-1]] += content
  # pprint(subelemStack)
  # pprint(holder)
  
class WikiContentHandler(sax.ContentHandler): 
  def startDocument(self):
    self.elemStack = []
    self.ignore = False

  def startElement(self, name, attrs):
    self.elemStack.append(name)
    if name == 'page':
      self.pageElems = {}
      self.revisions = []
    if name == 'revision':
      self.revisionElems = {}
    if name == 'text':
      self.ignore = True

  def characters(self, content):
    if self.ignore:
      return

    if 'page' not in self.elemStack or self.elemStack.index('page') == len(self.elemStack) - 1:
      return

    if 'revision' in self.elemStack:
      if self.elemStack.index('page') > self.elemStack.index('revision'):
        raise Error('Bad XML stack %s' % str(self.elemStack))
      if self.elemStack.index('revision') == len(self.elemStack) - 1:
        return

      addElem(self.elemStack[self.elemStack.index('revision') + 1:], self.revisionElems, content)
    else:
      addElem(self.elemStack[self.elemStack.index('page') + 1:], self.pageElems, content)

  def endElement(self, name):
    self.elemStack.pop()
    if name == 'text':
      self.ignore = False
    if name == 'page':
      for revision in self.revisions: 
        merged = {}
        merged.update(self.pageElems)
        merged.update(revision)
        json.dump(merged, sys.stdout)
        sys.stdout.write("\n")

      self.pageElems = {}
      self.revisions = []
    if name == 'revision':
      self.revisions.append(self.revisionElems)
      self.revisionElems = {}

sax.parse(sys.stdin, WikiContentHandler())
