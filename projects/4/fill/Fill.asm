// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// init loop counter
(INIT)
  @SCREEN
  D=A
(LOOP)
  // if at end of SCREEN goto INIT
  @24576 //16384+8192
  D=D-A
  @INIT
  D;JEQ
  // set next screen register
  @24576 //16384+8192
  D=D+A
  @R0
  M=D
  // get keyboard
  @KBD
  D=M
  // if 0, goto CLEAR
  @CLEAR
  D;JEQ
(BLACKEN)
  // get next screen register
  @R0
  A=M
  // blacken
  M=-1
(INCREMENT)
  // increment counter
  @R0
  D=M+1
  // goto LOOP
  @LOOP
  0;JMP
(CLEAR)
  // get next screen register
  @R0
  A=M
  // clear
  M=0
  // goto INCREMENT
  @INCREMENT
  0;JMP
