// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// init constant and memories
@R2
M=0
@i
M=0
// we'll check what operand is greater so we can iterate over the lesser by adding the greater to itself
// so we suppose here that R0 <= R1
@R0
D=M
@iter
M=D

@R1
D=M
@base
M=D

// check if R0 > R1
@R0
D=M-D
@CHNG_TEMP
D;JGT

(LOOP)
	// if (i = iter) goto STOP
	@iter
	D=M
	@i
	D=M-D
	@STOP
	D;JMP

	// R2 = R2 + base 
	@base
	D=M
	@R2
	M=M+D

	// i = i + 1
	@i
	M=M+1

	// goto LOOP
	@LOOP
	0;JMP

(STOP)
	@END
	0;JMP

// here that R1 > R0
(CHNG_TEMP)
	@R1
	D=M
	@iter
	M=D

	@R0
	D=M
	@base
	M=D

	@LOOP
	0;JMP

(END)
	0;JMP