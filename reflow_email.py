#!/usr/bin/python

# This script reflows emails so that all lines are shorter than a maximum length
# while preserving the quoting level indicated by leading '>' characters.

import re
import string
import sys

def reflow(lines):
  """Reflows a list of lines of an email.
  
  Args:
    lines: the original email in a file-like object
  Returns:
    the reflowed email as a single string
  """
  current_level = 0
  current_block = ''
  output = ''
  for raw_line in lines:
    line = unicode(raw_line.strip(), errors='ignore')
    level, text = parse_line(line)
    if level == current_level:
      current_block += ' ' + text
    else:
      output += render_text(current_block, current_level)
      current_level = level
      current_block = text
  output += render_text(current_block, current_level)
  return output

def parse_line(line):
  """Strips indentation indicators from a line and counts them.
  
  Args:
    line: a line, sans newline
  Returns:
    a tuple of indentation level and text without indentation indicators
  """
  match = re.search('^[\s>]*', line)
  return (string.count(match.group(0), '>'), line[match.end(0):])

def render_text(text, indentation_level):
  """Renders a block of text at the specified indentation level.
  
  Args:
    text: the text to split across lines
    indentation_level: the number of '>' to prefix
  Returns:
    the rendered block of indented text
  """
  prefix = '>' * indentation_level + ' '
  max_length = 72 - len(prefix)
  words = re.split('(?u)\s', text)
  output = ''
  line = ''
  for word in words:
    if not line:
      line = word
    else:
      if len(line) + len(word) < max_length:
        line += ' ' + word
      else:
        output += prefix + line + '\n'
        line = word
  if line:
    output += prefix + line + '\n'
  return output

print reflow(sys.stdin)