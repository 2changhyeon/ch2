# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 22:52:49 2021

@author: PC
"""

#stanza.download('en') # download English model
import re
import nltk
import stanza
nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt, pos')

replacement_patterns = [
    (r"\(", "\\\("),
    (r"\)", "\\\)"),
    (r"\[", "\\\["),
    (r"\]", "\\\]"),
    (r"\{", "\\\{"),
    (r"\}", "\\\}"), # 이모티콘을 인식하게 하기 위해서 대체했다.
    (r'won\'t', 'will not'),
    (r'don\'t', 'do not'),
    (r'can\'t', 'cannot'),
    (r'i\'m', 'i am'),
    (r'ain\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would'),
]

class RegexpReplacer(object):
  def __init__(self, patterns):
    self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
  
  def replace(self, text):
    s = text
    for (pattern, repl) in self.patterns:
      (s, count) = re.subn(pattern, repl, s)
    return s

def parenthreplace(text):  
  replacer = RegexpReplacer(replacement_patterns)
  return replacer.replace(text)

econlist = [
  ":-)", ":)", ":-(", ":(", ";)",
]
emojirange = "[\U000000A9\U000000AE\U0000203C\U00002049\U000020E3\U00002122\U00002139\U00002194-\U00002199\U000021A9-\U000021AA\U0000231A\U0000231B\U00002328\U000023CF\U000023E9-\U000023F3\U000023F8-\U000023FA\U000024C2\U000025AA\U000025AB\U000025B6\U000025C0\U000025FB-\U000025FE\U00002600-\U000027EF\U00002934\U00002935\U00002B00-\U00002BFF\U00003030\U0000303D\U00003297\U00003299\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F100-\U0001F64F\U0001F680-\U0001F6FF\U0001F910-\U0001F96B\U0001F980-\U0001F9E0]"

pat = ""
for econ in econlist:
  pat += parenthreplace(econ)
  pat += "|"
pat += emojirange
pat += r"|^\w+|'\w+|\S\w+|\S"

# 미리 정의해둔 econlist 내부의 이모티콘에게 'IMG' 태그를 달아주는 함수
def mod_tokentag(tokentag):
  new_tokentag = tokentag.copy()
  for i in range(len(tokentag)):
    token, tag = tokentag[i]
    if token in econlist:
      new_tokentag[i] = (token, 'IMG')
  return new_tokentag


def get_ztag(text):
  doc = nlp(text)
  l = list()
  for sent in doc.sentences:
    for word in sent.words:
      l.append(word.upos)
  return l

def get_tokentag(text):
  tokens = re.findall(pat, text)
  tags = get_ztag(text)
  tokentag = list(zip(tokens, tags))
  for i in range(len(tokentag)):
    token, tag = tokentag[i]
    l = re.findall(emojirange, token)
    if token in econlist:
      tokentag[i] = (token, 'IMG')
    elif len(l) != 0:
      if tag != 'NOUN':
        #print(l)
        tokentag[i] = (token, 'IMG')
  return tokentag 



img_rules = [
  'S -> IMGP S | S IMGP',
]
clause_rules = [
  'S -> ADVP S | INTJP S | CCONJ S',
  'S -> S PUNCT',
  'S -> S S', #multi sentence
  'SBAR -> NP VP',
  'S -> NP VP | NP',
  'S -> VP' # Direct question
]
phrase_rules = [
  'INTJP -> INTJ PUNCT',
  'VP -> VP ADJP | VP PART | VP VERB | VP ADV | VP NP | VP SBAR | VP PP | VP SCONJP | VP AUX',
  'NP -> DET NP | ADJ NP',
  'NP -> NP NOUN | NP PRON | NP PROPN',
  'PP -> PP NP'
]
upos_rules = [
  'NP -> NOUN | PRON | PROPN',
  'VP -> VERB | AUX',
  'ADJP -> ADJ SCONJP',
  'SCONJP -> SCONJ SBAR',
  'PP -> ADP',
  'IMGP -> IMG',
]
term_ruledict = {
  "ADJ" : "ADJ -> '(NONE)'",
  "ADP" : "ADP -> '(NONE)'",
  "ADV" : "ADV -> '(NONE)'",
  "AUX" : "AUX -> '(NONE)'",
  "CCONJ" : "CCONJ -> '(NONE)'",
  "DET" : "DET -> '(NONE)'",
  "INTJ" : "INTJ -> '(NONE)'",
  "PART" : "PART -> '(NONE)'",
  "NOUN" : "NOUN -> '(NONE)'",
  "PRON" : "PRON -> '(NONE)'",
  "PROPN" : "PROPN -> '(NONE)'",
  "PUNCT" : "PUNCT -> '(NONE)'",
  "SCONJ" : "SCONJ -> '(NONE)'",
  "VERB" : "VERB -> '(NONE)'",    
  "IMG" : "IMG -> '(NONE)'",
}

def attach_term(tok_tag):
  new_term_ruledict = term_ruledict.copy()
  for token, tag in tok_tag:
    new_term_ruledict[tag] += "|'"
    new_term_ruledict[tag] += token
    new_term_ruledict[tag] += "'"
  rules = list()
  rules.extend(clause_rules)
  rules.extend(phrase_rules)
  rules.extend(img_rules)
  rules.extend(upos_rules)
  rules.extend(new_term_ruledict.values())
  rule = ""
  for ruleline in rules:
    rule += ruleline
    rule += "\n"
  return rule

def BULCCParserExample(grammar, text, tok_tag):
  parser = nltk.parse.BottomUpLeftCornerChartParser(grammar)
  sentence = list()
  for token, tag in tok_tag:
    sentence.append(token)
  chart = parser.chart_parse(sentence)
  #print((chart.num_edges()))
  parses = list(chart.parses(grammar.start()))
  #print(len(parses))
  for tree in parses:
    tree.pretty_print()
    break


text =   "Auts 😩 I bet that tomorrow will be a better day… 😍"






tok_tag = get_tokentag(text)
print(tok_tag)

grammar = nltk.CFG.fromstring(attach_term(tok_tag))
BULCCParserExample(grammar, text, tok_tag)








