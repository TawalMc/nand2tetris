// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// init constants

// target screen color
@target_color
M=0

// current screen color
@curr_color
M=0

// KBD max addr = 16384 + 8191 - 1

(LOOP)
	// check if kbd is pressed
	@KBD
	D=M
	@BLACK_SCREEN
	D;JGT
	@WHITE_SCREEN
	D;JEQ

	@LOOP
	0;JMP

(BLACK_SCREEN)
	@target_color
	M=-1
	@UPDATE_SCREEN
	0;JMP

(WHITE_SCREEN)
	@target_color
	M=0
	@UPDATE_SCREEN
	0;JMP

(UPDATE_SCREEN)
	// if already black (curr_color = target_color) just jump to loop
	@curr_color
	D=M
	@target_color
	D=M-D
	@LOOP
	D;JEQ

	// if (curr_color != target_color)
	@i
	M=0
	(UPDATE_SCREEN_LOOP)
		// compare i and R0
		@i
		D=M
		@R0
		D=D-M
		@INIT_CONST
		D;JGT

		// fill the screen with target color
		@SCREEN
		D=A
		@i
		A=D+M
		D=A
		@temp
		M=D
		@target_color
		D=M
		@temp
		A=M
		M=D

		// i=i+1
		@i
		M=M+1

		@UPDATE_SCREEN_LOOP
		0;JMP

// set current_color to the target color
(INIT_CONST)
	@target_color
	D=M
	@curr_color
	M=D
	@LOOP
	0;JMP