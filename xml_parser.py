#!/usr/bin/env python3
"""xml_parser - Lightweight XML parser with XPath-like queries."""
import sys, json, re

class XmlNode:
    def __init__(self, tag, attrs=None, children=None, text=""):
        self.tag = tag; self.attrs = attrs or {}; self.children = children or []; self.text = text
    def find(self, tag):
        for c in self.children:
            if c.tag == tag: return c
        return None
    def find_all(self, tag): return [c for c in self.children if c.tag == tag]

def parse_xml(text):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return _parse(text.strip(), 0)[0]

def _parse(text, pos):
    while pos < len(text) and text[pos] != '<': pos += 1
    if pos >= len(text): return None, pos
    m = re.match(r'<(\w+)((?:\s+\w+=["\'][^"\']*["\'])*)\s*(/?)>', text[pos:])
    if not m: return None, pos + 1
    tag = m.group(1)
    attrs = dict(re.findall(r'(\w+)=["\']([^"\']*)["\']', m.group(2)))
    if m.group(3) == '/': return XmlNode(tag, attrs), pos + m.end()
    pos += m.end(); content = ""; children = []
    end_tag = '</' + tag + '>'
    while pos < len(text):
        if text[pos:pos+len(end_tag)] == end_tag:
            return XmlNode(tag, attrs, children, content), pos + len(end_tag)
        if text[pos] == '<' and not text[pos:].startswith('</'):
            child, pos = _parse(text, pos)
            if child: children.append(child)
        else: content += text[pos]; pos += 1
    return XmlNode(tag, attrs, children, content), pos

def main():
    xml = '<library><book id="1"><title>Gatsby</title><author>Fitzgerald</author></book><book id="2"><title>1984</title><author>Orwell</author></book></library>'
    root = parse_xml(xml)
    print("XML parser demo\n")
    for b in root.find_all("book"):
        t = b.find("title").text if b.find("title") else "?"
        a = b.find("author").text if b.find("author") else "?"
        print(f'  [{b.attrs.get("id")}] {t} by {a}')

if __name__ == "__main__":
    main()
