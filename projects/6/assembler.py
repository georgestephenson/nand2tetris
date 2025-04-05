#!/usr/bin/python
import sys
from enum import Enum

class InstructionType(Enum):
  A_INSTRUCTION = 1,
  C_INSTRUCTION = 2,
  L_INSTRUCTION = 3

class Parser:
  def __init__(self, filename: str):
    with open(filename) as f:
      self.lines = f.readlines()
    self.next_line = 0
    self.instruction = ''

  def has_more_lines(self):
    return self.next_line < len(self.lines)
  
  def advance(self):
    line_text = self.lines[self.next_line].strip()
    self.next_line += 1
    if line_text and not line_text.startswith('//'):
      self.instruction = line_text
    else:
      self.instruction = ''
      if self.has_more_lines():
        self.advance()

  def instruction_type(self):
    if self.instruction[0] == '@':
      return InstructionType.A_INSTRUCTION
    elif self.instruction.startswith('(') and self.instruction.endswith(')'):
      return InstructionType.L_INSTRUCTION
    else:
      return InstructionType.C_INSTRUCTION
    
  def symbol(self):
    if self.instruction[0] == '@':
      return self.instruction[1:]
    else:
      return self.instruction[1:-1]
    
  def dest(self):
    try:
      eq_idx = self.instruction.index('=')
    except ValueError:
      return ''
    return self.instruction[:eq_idx]
  
  def comp(self):
    try:
      eq_idx = self.instruction.index('=')
    except ValueError:
      eq_idx = -1
    try:
      sc_idx = self.instruction.index(';')
    except ValueError:
      sc_idx = len(self.instruction)
    return self.instruction[eq_idx+1:sc_idx]

  def jump(self):
    try:
      sc_idx = self.instruction.index(';')
    except ValueError:
      return ''
    return self.instruction[sc_idx+1:]

class Code:
  def dest(self, symbol: str) -> str:
    if not symbol:
      return '000'
    code = ['0','0','0']
    if 'A' in symbol:
      code[0]='1'
    if 'D' in symbol:
      code[1]='1'
    if 'M' in symbol:
      code[2]='1'    
    return "".join(code)
  
  def comp(self, symbol: str) -> str:
    if not symbol:
      raise ValueError('Instruction must have a comp mnemonic symbol')
    # not clever, but I think this is probably fastest
    if symbol=='0':
      return '0101010'
    if symbol=='1':
      return '0111111'
    if symbol=='-1':
      return '0111010'
    if symbol=='D':
      return '0001100'
    if symbol=='D+1':
      return '0011111'
    if symbol=='D-1':
      return '0001110'
    if 'M' in symbol:
      a = '1'
    else:
      a = '0'
    wild = symbol.replace('A','*').replace('M','*')
    if wild=='*':
      return a+'110000'
    if wild=='!*':
      return a+'110001'
    if wild=='-*':
      return a+'110011'
    if wild=='*+1':
      return a+'110111'
    if wild=='*-1':
      return a+'110010'
    if wild=='D+*':
      return a+'000010'
    if wild=='D-*':
      return a+'010011'
    if wild=='*-D':
      return a+'000111'
    if wild=='D&*':
      return a+'000000'
    if wild=='D|*':
      return a+'010101'
    raise ValueError('Comp mnemonic symbol not found')
  
  def jump(self, symbol: str) -> str:
    if not symbol:
      return '000'
    if symbol == 'JGT':
      return '001'
    if symbol == 'JEQ':
      return '010'
    if symbol == 'JGE':
      return '011'
    if symbol == 'JLT':
      return '100'
    if symbol == 'JNE':
      return '101'
    if symbol == 'JLE':
      return '110'
    if symbol == 'JMP':
      return '111'
    raise ValueError('Jump mnemonic symbol not found')

filename = sys.argv[1]
if not filename.endswith(".asm"):
  raise ValueError('Filename must end with .asm')
print('Assembling ' + filename)
parser = Parser(filename)
code = Code()
f = open(filename.replace('.asm','.hack',1),'w')
while(parser.has_more_lines()):
  parser.advance()
  if not parser.instruction:
    continue
  instruction_type = parser.instruction_type()
  if instruction_type==InstructionType.A_INSTRUCTION:
    numberInt = int(parser.symbol())
    numberBin = format(numberInt, '015b')
    binary = '0' + numberBin
    f.write(binary + '\n')
  elif instruction_type==InstructionType.C_INSTRUCTION:
    dest = code.dest(parser.dest())
    comp = code.comp(parser.comp())
    jump = code.jump(parser.jump())
    binary = '111' + comp + dest + jump
    f.write(binary + '\n')
f.close()