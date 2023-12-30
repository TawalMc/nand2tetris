// init i with RO value
@R0
D=M
@i
M=D

// init sum with R1 value
@R1
D=M
@sum
M=D

// init t with R4 value
@R4
D=M
@t
M=D

// compute sum = sum + i
@i
D=M
@sum
M=M+D

// end
@END
0;JMP

(END)
	@END
	0;JMP