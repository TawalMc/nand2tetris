
//Class1.vm
(Class1.set)
@Class1.set$i
M=0
(Class1.set$LOOP_0)
@0
D=A
@Class1.set$i
D=D-M
@Class1.set$END_LOOP_0
D;JLE
@SP
A=M
M=0
@SP
M=M+1
@Class1.set$i
M=M+1
@Class1.set$LOOP_0
0; JMP
(Class1.set$END_LOOP_0)
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
@SP
A=M-1
D=M
@StaticsTest.0
M=D
@SP
M=M-1
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
@SP
A=M-1
D=M
@StaticsTest.1
M=D
@SP
M=M-1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@Class1.set$END_FRAME
M=D
@5
D=A
@Class1.set$END_FRAME
A=M-D
D=M
@Class1.set$RET_ADDR
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@1
D=A
@ARG
D=M+D
@SP
M=D
@1
D=A
@Class1.set$END_FRAME
A=M-D
D=M
@THAT
M=D
@2
D=A
@Class1.set$END_FRAME
A=M-D
D=M
@THIS
M=D
@3
D=A
@Class1.set$END_FRAME
A=M-D
D=M
@ARG
M=D
@4
D=A
@Class1.set$END_FRAME
A=M-D
D=M
@LCL
M=D
@Class1.set$RET_ADDR
A=M
0;JMP
(Class1.get)
@Class1.get$i
M=0
(Class1.get$LOOP_1)
@0
D=A
@Class1.get$i
D=D-M
@Class1.get$END_LOOP_1
D;JLE
@SP
A=M
M=0
@SP
M=M+1
@Class1.get$i
M=M+1
@Class1.get$LOOP_1
0; JMP
(Class1.get$END_LOOP_1)
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@StaticsTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@LCL
D=M
@Class1.get$END_FRAME
M=D
@5
D=A
@Class1.get$END_FRAME
A=M-D
D=M
@Class1.get$RET_ADDR
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@1
D=A
@ARG
D=M+D
@SP
M=D
@1
D=A
@Class1.get$END_FRAME
A=M-D
D=M
@THAT
M=D
@2
D=A
@Class1.get$END_FRAME
A=M-D
D=M
@THIS
M=D
@3
D=A
@Class1.get$END_FRAME
A=M-D
D=M
@ARG
M=D
@4
D=A
@Class1.get$END_FRAME
A=M-D
D=M
@LCL
M=D
@Class1.get$RET_ADDR
A=M
0;JMP

//Class2.vm
(Class2.set)
@Class2.set$i
M=0
(Class2.set$LOOP_2)
@0
D=A
@Class2.set$i
D=D-M
@Class2.set$END_LOOP_2
D;JLE
@SP
A=M
M=0
@SP
M=M+1
@Class2.set$i
M=M+1
@Class2.set$LOOP_2
0; JMP
(Class2.set$END_LOOP_2)
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
@SP
A=M-1
D=M
@StaticsTest.0
M=D
@SP
M=M-1
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
@SP
A=M-1
D=M
@StaticsTest.1
M=D
@SP
M=M-1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@Class2.set$END_FRAME
M=D
@5
D=A
@Class2.set$END_FRAME
A=M-D
D=M
@Class2.set$RET_ADDR
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@1
D=A
@ARG
D=M+D
@SP
M=D
@1
D=A
@Class2.set$END_FRAME
A=M-D
D=M
@THAT
M=D
@2
D=A
@Class2.set$END_FRAME
A=M-D
D=M
@THIS
M=D
@3
D=A
@Class2.set$END_FRAME
A=M-D
D=M
@ARG
M=D
@4
D=A
@Class2.set$END_FRAME
A=M-D
D=M
@LCL
M=D
@Class2.set$RET_ADDR
A=M
0;JMP
(Class2.get)
@Class2.get$i
M=0
(Class2.get$LOOP_3)
@0
D=A
@Class2.get$i
D=D-M
@Class2.get$END_LOOP_3
D;JLE
@SP
A=M
M=0
@SP
M=M+1
@Class2.get$i
M=M+1
@Class2.get$LOOP_3
0; JMP
(Class2.get$END_LOOP_3)
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@StaticsTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@LCL
D=M
@Class2.get$END_FRAME
M=D
@5
D=A
@Class2.get$END_FRAME
A=M-D
D=M
@Class2.get$RET_ADDR
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@1
D=A
@ARG
D=M+D
@SP
M=D
@1
D=A
@Class2.get$END_FRAME
A=M-D
D=M
@THAT
M=D
@2
D=A
@Class2.get$END_FRAME
A=M-D
D=M
@THIS
M=D
@3
D=A
@Class2.get$END_FRAME
A=M-D
D=M
@ARG
M=D
@4
D=A
@Class2.get$END_FRAME
A=M-D
D=M
@LCL
M=D
@Class2.get$RET_ADDR
A=M
0;JMP

//Sys.vm
(Sys.init)
@Sys.init$i
M=0
(Sys.init$LOOP_4)
@0
D=A
@Sys.init$i
D=D-M
@Sys.init$END_LOOP_4
D;JLE
@SP
A=M
M=0
@SP
M=M+1
@Sys.init$i
M=M+1
@Sys.init$LOOP_4
0; JMP
(Sys.init$END_LOOP_4)
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@5
M=D
@SP
M=M-1
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
D=M
@5
M=D
@SP
M=M-1
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
