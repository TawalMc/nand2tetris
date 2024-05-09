

//FibonacciSeries.vm
// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1           // that = argument[1]
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0              // first element in the series = 0
@0
D=A
@THAT
D=M+D
@addr
M=D
@SP
A=M-1
D=M
@addr
A=M
M=D
@SP
M=M-1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1              // second element in the series = 1
@1
D=A
@THAT
D=M+D
@addr
M=D
@SP
A=M-1
D=M
@addr
A=M
M=D
@SP
M=M-1
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// pop argument 0          // num_of_elements -= 2 (first 2 elements are set)
@0
D=A
@ARG
D=M+D
@addr
M=D
@SP
A=M-1
D=M
@addr
A=M
M=D
@SP
M=M-1
// label MAIN_LOOP_START
(null$MAIN_LOOP_START)
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT // if num_of_elements > 0, goto COMPUTE_ELEMENT
@SP
A=M-1
D=M
@SP
M=M-1
@null$COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM        // otherwise, goto END_PROGRAM
@null$END_PROGRAM
0;JMP
// label COMPUTE_ELEMENT
(null$COMPUTE_ELEMENT)
// push that 0
@0
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@1
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
M=M-1
// pop that 2              // that[2] = that[0] + that[1]
@2
D=A
@THAT
D=M+D
@addr
M=D
@SP
A=M-1
D=M
@addr
A=M
M=D
@SP
M=M-1
// push pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
M=M-1
// pop pointer 1           // that += 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// pop argument 0          // num_of_elements--
@0
D=A
@ARG
D=M+D
@addr
M=D
@SP
A=M-1
D=M
@addr
A=M
M=D
@SP
M=M-1
// goto MAIN_LOOP_START
@null$MAIN_LOOP_START
0;JMP
// label END_PROGRAM
(null$END_PROGRAM)
