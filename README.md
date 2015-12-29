MIPS-Simulator
==============
###Program description

A simulator that can load and run full MIPS programs (similar to, but more basic than SPIM or MARS).
The simulator runs on the command line and takes as input a text file.

****

###How to run

Run test_cpu.py with the following format:
>python test_cpu.py [instruction_file]

For example:
>python test_cpu.py testFiles/printTriangle.txt

The following instruction files are provided in testFiles folder:

1. count.txt - Prints out 1 to 10

2. fizzbuzz.txt - Prints out the FizzBuzz program

3. HelloWorld.txt - Prints out "Hello, World!"

4. printTriangle.txt - Prints out the Pascal triangle with custom size.

****

###Input description

 1. The file format of the input is in the ASCII format, rather than the binary format.   
 2. Lines of the file will specify either memory values or register values.
A line that specifies a memory location will give an address followed by some number of memory words, all expressed in hex, and beginning with the prefix "0x".
The memory location comes first and is placed in square brackets [].

*Example 1:*
>[R13] 0x0000ffff
>[PC] 0x00004000

The following line contains an add immediate instruction that adds the value 4 to register $29 and stores the result in register $5.

*Example 2:*
>[0x00400004] 0x27a50004        #addiu $5, $29, 4;        184: addiu $a1, $sp, 4

Only the first two hex values matter; the rest of the line, which lists the generated code in assembly format, and the input line from which it was assembled, can be considered a comment.

Address A=[0x00400004] is a byte address. Since words (ints) are 4 bytes long, the index in your memory array should be A/4. Thus, if V=0x27a50004 is the value on the line, and MEM is the name of your memory array, your code might have a line like:
>MEM[A/4] = V;

Another example, which contains multiple data words on the same line, and is given as follows:

    [0x00010000]  0x6c6c6548  0x6f57206f  0x00646c72  0x00000000
In this case, the 4 words spell out the text "Hello World" in ASCII. The encoding places the low order byte first in the character stream. Consequently, the word 0x6c6c6548 spells out the letters "Hell", but from right to left (e.g. 0x48='H', 0x65='e', and 0x6c='l').

**The sample input files can be found in 'testFiles' folder.**
****
### Supported MIPS instructions:

| Instructions | Encoding                           | Operation                                                                             |
| ---          | ---                                | ---                                                                                   |
| add          | 0b00000000000000000000000000100000 | $d = $s + $t; advance_pc (4);                                                         |
| addi         | 0b00100000000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addiu        | 0b00100100000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addu         | 0b00000000000000000000000000100001 | $d = $s + $t; advance_pc (4);                                                         |
| and          | 0b00000000000000000000000000100100 | $d = $s & $t; advance_pc (4);                                                         |
| andi         | 0b00110000000000000000000000000000 | $t = $s & imm; advance_pc (4);                                                        |
| beq          | 0b00010000000000000000000000000000 | if $s == $t advance_pc (offset << 2)); else advance_pc (4);                           |
| bgez         | 0b00000100000000010000000000000000 | if $s >= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bgezal       | 0b00000100000100010000000000000000 | if $s >= 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4); |
| bgtz         | 0b00011100000000000000000000000000 | if $s > 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| blez         | 0b00011000000000000000000000000000 | if $s <= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bltz         | 0b00000100000000000000000000000000 | if $s < 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| bltzal       | 0b00000100000100000000000000000000 | if $s < 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4);  |
| bne          | 0b00010100000000000000000000000000 | if $s != $t advance_pc (offset << 2)); else advance_pc (4);                           |
| div          | 0b00000000000000000000000000011010 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| divu         | 0b00000000000000000000000000011011 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| j - jump     | 0b00001000000000000000000000000000 | PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);                               |
| jal          | 0b00001100000000000000000000000000 | $31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);    |
| jr           | 0b00000000000000000000000000001000 | PC = nPC; nPC = $s;                                                                   |
| lb           | 0b10000000000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| lui          | 0b00111100000000000000000000000000 | $t = (imm << 16); advance_pc (4);                                                     |
| lw           | 0b10001100000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| mfhi         | 0b00000000000000000000000000010000 | $d = $HI; advance_pc (4);                                                             |
| mflo         | 0b00000000000000000000000000010010 | $d = $LO; advance_pc (4);                                                             |
| mult         | 0b00000000000000000000000000011000 | $LO = $s * $t; advance_pc (4);                                                        |
| multu        | 0b00000000000000000000000000011001 | $LO = $s * $t; advance_pc (4);                                                        |
| noop         | 0b00000000000000000000000000000000 | advance_pc (4);                                                                       |
| or           | 0b00000000000000000000000000100101 | $d = $s &#124; $t; advance_pc (4);                                                    |
| ori          | 0b00110100000000000000000000000000 | $t = $s &#124; imm; advance_pc (4);                                                   |
| sb           | 0b10100000000000000000000000000000 | MEM[$s + offset] = (0xff & $t); advance_pc (4);                                       |
| sll          | 0b00000000000000000000000000000000 | $d = $t << h; advance_pc (4);                                                         |
| sllv         | 0b00000000000000000000000000000100 | $d = $t << $s; advance_pc (4)                                                         |
| slt          | 0b00000000000000000000000000101010 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| slti         | 0b00101000000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltiu        | 0b00101100000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltu         | 0b00000000000000000000000000101011 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| sra          | 0b00000000000000000000000000000011 | $d = $t >> h; advance_pc (4);                                                         |
| srl          | 0b00000000000000000000000000000010 | $d = $t >> h; advance_pc (4);                                                         |
| srlv         | 0b00000000000000000000000000000110 | $d = $t >> $s; advance_pc (4);                                                        |
| sub          | 0b00000000000000000000000000100010 | $d = $s - $t; advance_pc (4);                                                         |
| subu         | 0b00000000000000000000000000100011 | $d = $s - $t; advance_pc (4);                                                         |
| sw           | 0b10101100000000000000000000000000 | MEM[$s + offset] = $t; advance_pc (4);                                                |
| syscall      | 0b00000000000000000000000000001100 | advance_pc (4)                                                                        |
| xor          | 0b00000000000000000000000000100110 | $d = $s ^ $t; advance_pc (4);                                                         |
| xori         | 0b00111000000000000000000000000000 | $t = $s ^ imm; advance_pc (4);                                                        |
****
### Supported System calls:
| Value | Name                          | Description                                                                             |
| ---          | ---                                | ---                                                                                   |
| (1)          | Print integer | Prints an integer held in register $a0=$4.|
| (4)          | Print string  | Prints a null-terminated string, where $a0  points to the string. Note that the string will be stored as consecutive bytes in your memory array (of ints), so you will have to deal with the differences.   
| (5)          | Read integer | Reads an integer from stdin (the keyboard), place it in register $v0=$2.|
| (8)          | Read string | Reads a string into address pointed to by $a0=$4, up to $a1-1 characters, and null terminates the string. Note that the characters must be stored as bytes, so you will have to deal with converting a string from the language used for your simulator to a null terminated string stored in an array of ints.|
| (9)          | Allocate memory | Allocates bytes based on $a0=$4, returns address in $v0=$2|
| (10)          | Exit | Exits the program, stopping the simulator.|
MIPS-Simulator
==============
###Program description

A simulator that can load and run full MIPS programs (similar to, but more basic than SPIM or MARS).
The simulator runs on the command line and takes as input a text file.

****

###Input description

 1. The file format of the input is in the ASCII format, rather than the binary format.   
 2. Lines of the file will specify either memory values or register values.
A line that specifies a memory location will give an address followed by some number of memory words, all expressed in hex, and beginning with the prefix "0x".
The memory location comes first and is placed in square brackets [].

*Example 1:*
>[R13] 0x0000ffff
>[PC] 0x00004000

The following line contains an add immediate instruction that adds the value 4 to register $29 and stores the result in register $5.

*Example 2:*
>[0x00400004] 0x27a50004        #addiu $5, $29, 4;        184: addiu $a1, $sp, 4

Only the first two hex values matter; the rest of the line, which lists the generated code in assembly format, and the input line from which it was assembled, can be considered a comment.

Address A=[0x00400004] is a byte address. Since words (ints) are 4 bytes long, the index in your memory array should be A/4. Thus, if V=0x27a50004 is the value on the line, and MEM is the name of your memory array, your code might have a line like:
>MEM[A/4] = V;

Another example, which contains multiple data words on the same line, and is given as follows:

    [0x00010000]  0x6c6c6548  0x6f57206f  0x00646c72  0x00000000
In this case, the 4 words spell out the text "Hello World" in ASCII. The encoding places the low order byte first in the character stream. Consequently, the word 0x6c6c6548 spells out the letters "Hell", but from right to left (e.g. 0x48='H', 0x65='e', and 0x6c='l').

**The sample input files can be found in 'testFiles' folder.**

****
### Supported MIPS instructions:

| Instructions | Encoding                           | Operation                                                                             |
| ---          | ---                                | ---                                                                                   |
| add          | 0b00000000000000000000000000100000 | $d = $s + $t; advance_pc (4);                                                         |
| addi         | 0b00100000000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addiu        | 0b00100100000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addu         | 0b00000000000000000000000000100001 | $d = $s + $t; advance_pc (4);                                                         |
| and          | 0b00000000000000000000000000100100 | $d = $s & $t; advance_pc (4);                                                         |
| andi         | 0b00110000000000000000000000000000 | $t = $s & imm; advance_pc (4);                                                        |
| beq          | 0b00010000000000000000000000000000 | if $s == $t advance_pc (offset << 2)); else advance_pc (4);                           |
| bgez         | 0b00000100000000010000000000000000 | if $s >= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bgezal       | 0b00000100000100010000000000000000 | if $s >= 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4); |
| bgtz         | 0b00011100000000000000000000000000 | if $s > 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| blez         | 0b00011000000000000000000000000000 | if $s <= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bltz         | 0b00000100000000000000000000000000 | if $s < 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| bltzal       | 0b00000100000100000000000000000000 | if $s < 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4);  |
| bne          | 0b00010100000000000000000000000000 | if $s != $t advance_pc (offset << 2)); else advance_pc (4);                           |
| div          | 0b00000000000000000000000000011010 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| divu         | 0b00000000000000000000000000011011 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| j - jump     | 0b00001000000000000000000000000000 | PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);                               |
| jal          | 0b00001100000000000000000000000000 | $31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);    |
| jr           | 0b00000000000000000000000000001000 | PC = nPC; nPC = $s;                                                                   |
| lb           | 0b10000000000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| lui          | 0b00111100000000000000000000000000 | $t = (imm << 16); advance_pc (4);                                                     |
| lw           | 0b10001100000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| mfhi         | 0b00000000000000000000000000010000 | $d = $HI; advance_pc (4);                                                             |
PS-Simulator
==============
###Program description

A simulator that can load and run full MIPS programs (similar to, but more basic than SPIM or MARS).
The simulator runs on the command line and takes as input a text file.

****

###How to run

Run test_cpu.py with the following format:
>python test_cpu.py [instruction_file]

For example:
>python test_cpu.py testFiles/printTriangle.txt

The following instruction files are provided in testFiles folder:
1. count.txt - Prints out 1 to 10
2. fizzbuzz.txt - Prints out the FizzBuzz program
3. HelloWorld.txt - Prints out "Hello, World!"
4. printTriangle.txt - Prints out the Pascal triangle with custom size.

****

###Input description

 1. The file format of the input is in the ASCII format, rather than the binary format.   
 2. Lines of the file will specify either memory values or register values.
A line that specifies a memory location will give an address followed by some number of memory words, all expressed in hex, and beginning with the prefix "0x".
The memory location comes first and is placed in square brackets [].

*Example 1:*
>[R13] 0x0000ffff
>[PC] 0x00004000

The following line contains an add immediate instruction that adds the value 4 to register $29 and stores the result in register $5.

*Example 2:*
>[0x00400004] 0x27a50004        #addiu $5, $29, 4;        184: addiu $a1, $sp, 4

Only the first two hex values matter; the rest of the line, which lists the generated code in assembly format, and the input line from which it was assembled, can be considered a comment.

Address A=[0x00400004] is a byte address. Since words (ints) are 4 bytes long, the index in your memory array should be A/4. Thus, if V=0x27a50004 is the value on the line, and MEM is the name of your memory array, your code might have a line like:
>MEM[A/4] = V;

Another example, which contains multiple data words on the same line, and is given as follows:

    [0x00010000]  0x6c6c6548  0x6f57206f  0x00646c72  0x00000000
In this case, the 4 words spell out the text "Hello World" in ASCII. The encoding places the low order byte first in the character stream. Consequently, the word 0x6c6c6548 spells out the letters "Hell", but from right to left (e.g. 0x48='H', 0x65='e', and 0x6c='l').

**The sample input files can be found in 'testFiles' folder.**
****
### Supported MIPS instructions:

| Instructions | Encoding                           | Operation                                                                             |
| ---          | ---                                | ---                                                                                   |
| add          | 0b00000000000000000000000000100000 | $d = $s + $t; advance_pc (4);                                                         |
| addi         | 0b00100000000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addiu        | 0b00100100000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addu         | 0b00000000000000000000000000100001 | $d = $s + $t; advance_pc (4);                                                         |
| and          | 0b00000000000000000000000000100100 | $d = $s & $t; advance_pc (4);                                                         |
| andi         | 0b00110000000000000000000000000000 | $t = $s & imm; advance_pc (4);                                                        |
| beq          | 0b00010000000000000000000000000000 | if $s == $t advance_pc (offset << 2)); else advance_pc (4);                           |
| bgez         | 0b00000100000000010000000000000000 | if $s >= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bgezal       | 0b00000100000100010000000000000000 | if $s >= 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4); |
| bgtz         | 0b00011100000000000000000000000000 | if $s > 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| blez         | 0b00011000000000000000000000000000 | if $s <= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bltz         | 0b00000100000000000000000000000000 | if $s < 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| bltzal       | 0b00000100000100000000000000000000 | if $s < 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4);  |
| bne          | 0b00010100000000000000000000000000 | if $s != $t advance_pc (offset << 2)); else advance_pc (4);                           |
| div          | 0b00000000000000000000000000011010 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| divu         | 0b00000000000000000000000000011011 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| j - jump     | 0b00001000000000000000000000000000 | PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);                               |
| jal          | 0b00001100000000000000000000000000 | $31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);    |
| jr           | 0b00000000000000000000000000001000 | PC = nPC; nPC = $s;                                                                   |
| lb           | 0b10000000000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| lui          | 0b00111100000000000000000000000000 | $t = (imm << 16); advance_pc (4);                                                     |
| lw           | 0b10001100000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| mfhi         | 0b00000000000000000000000000010000 | $d = $HI; advance_pc (4);                                                             |
| mflo         | 0b00000000000000000000000000010010 | $d = $LO; advance_pc (4);                                                             |
| mult         | 0b00000000000000000000000000011000 | $LO = $s * $t; advance_pc (4);                                                        |
| multu        | 0b00000000000000000000000000011001 | $LO = $s * $t; advance_pc (4);                                                        |
| noop         | 0b00000000000000000000000000000000 | advance_pc (4);                                                                       |
| or           | 0b00000000000000000000000000100101 | $d = $s &#124; $t; advance_pc (4);                                                    |
| ori          | 0b00110100000000000000000000000000 | $t = $s &#124; imm; advance_pc (4);                                                   |
| sb           | 0b10100000000000000000000000000000 | MEM[$s + offset] = (0xff & $t); advance_pc (4);                                       |
| sll          | 0b00000000000000000000000000000000 | $d = $t << h; advance_pc (4);                                                         |
| sllv         | 0b00000000000000000000000000000100 | $d = $t << $s; advance_pc (4)                                                         |
| slt          | 0b00000000000000000000000000101010 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| slti         | 0b00101000000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltiu        | 0b00101100000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltu         | 0b00000000000000000000000000101011 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| sra          | 0b00000000000000000000000000000011 | $d = $t >> h; advance_pc (4);                                                         |
| srl          | 0b00000000000000000000000000000010 | $d = $t >> h; advance_pc (4);                                                         |
| srlv         | 0b00000000000000000000000000000110 | $d = $t >> $s; advance_pc (4);                                                        |
| sub          | 0b00000000000000000000000000100010 | $d = $s - $t; advance_pc (4);                                                         |
| subu         | 0b00000000000000000000000000100011 | $d = $s - $t; advance_pc (4);                                                         |
| sw           | 0b10101100000000000000000000000000 | MEM[$s + offset] = $t; advance_pc (4);                                                |
| syscall      | 0b00000000000000000000000000001100 | advance_pc (4)                                                                        |
| xor          | 0b00000000000000000000000000100110 | $d = $s ^ $t; advance_pc (4);                                                         |
| xori         | 0b00111000000000000000000000000000 | $t = $s ^ imm; advance_pc (4);                                                        |
****
### Supported System calls:
| Value | Name                          | Description                                                                             |
| ---          | ---                                | ---                                                                                   |
| (1)          | Print integer | Prints an integer held in register $a0=$4.|
| (4)          | Print string  | Prints a null-terminated string, where $a0  points to the string. Note that the string will be stored as consecutive bytes in your memory array (of ints), so you will have to deal with the differences.   
| (5)          | Read integer | Reads an integer from stdin (the keyboard), place it in register $v0=$2.|
| (8)          | Read string | Reads a string into address pointed to by $a0=$4, up to $a1-1 characters, and null terminates the string. Note that the characters must be stored as bytes, so you will have to deal with converting a string from the language used for your simulator to a null terminated string stored in an array of ints.|
| (9)          | Allocate memory | Allocates bytes based on $a0=$4, returns address in $v0=$2|
| (10)          | Exit | Exits the program, stopping the simulator.|
| mflo         | 0b00000000000000000000000000010010 | $d = $LO; advance_pc (4);                                                             |IPS-Simulator
==============
###Program description

A simulator that can load and run full MIPS programs (similar to, but more basic than SPIM or MARS).
The simulator runs on the command line and takes as input a text file.

****

###Input description

 1. The file format of the input is in the ASCII format, rather than the binary format.   
 2. Lines of the file will specify either memory values or register values.
A line that specifies a memory location will give an address followed by some number of memory words, all expressed in hex, and beginning with the prefix "0x".
The memory location comes first and is placed in square brackets [].

*Example 1:*
>[R13] 0x0000ffff
>[PC] 0x00004000

The following line contains an add immediate instruction that adds the value 4 to register $29 and stores the result in register $5.

*Example 2:*
>[0x00400004] 0x27a50004        #addiu $5, $29, 4;        184: addiu $a1, $sp, 4

Only the first two hex values matter; the rest of the line, which lists the generated code in assembly format, and the input line from which it was assembled, can be considered a comment.

Address A=[0x00400004] is a byte address. Since words (ints) are 4 bytes long, the index in your memory array should be A/4. Thus, if V=0x27a50004 is the value on the line, and MEM is the name of your memory array, your code might have a line like:
>MEM[A/4] = V;

Another example, which contains multiple data words on the same line, and is given as follows:

    [0x00010000]  0x6c6c6548  0x6f57206f  0x00646c72  0x00000000
In this case, the 4 words spell out the text "Hello World" in ASCII. The encoding places the low order byte first in the character stream. Consequently, the word 0x6c6c6548 spells out the letters "Hell", but from right to left (e.g. 0x48='H', 0x65='e', and 0x6c='l').

**The sample input files can be found in 'testFiles' folder.**
****
### Supported MIPS instructions:

| Instructions | Encoding                           | Operation                                                                             |
| ---          | ---                                | ---                                                                                   |
| add          | 0b00000000000000000000000000100000 | $d = $s + $t; advance_pc (4);                                                         |
| addi         | 0b00100000000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addiu        | 0b00100100000000000000000000000000 | $t = $s + imm; advance_pc (4);                                                        |
| addu         | 0b00000000000000000000000000100001 | $d = $s + $t; advance_pc (4);                                                         |
| and          | 0b00000000000000000000000000100100 | $d = $s & $t; advance_pc (4);                                                         |
| andi         | 0b00110000000000000000000000000000 | $t = $s & imm; advance_pc (4);                                                        |
| beq          | 0b00010000000000000000000000000000 | if $s == $t advance_pc (offset << 2)); else advance_pc (4);                           |
| bgez         | 0b00000100000000010000000000000000 | if $s >= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bgezal       | 0b00000100000100010000000000000000 | if $s >= 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4); |
| bgtz         | 0b00011100000000000000000000000000 | if $s > 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| blez         | 0b00011000000000000000000000000000 | if $s <= 0 advance_pc (offset << 2)); else advance_pc (4);                            |
| bltz         | 0b00000100000000000000000000000000 | if $s < 0 advance_pc (offset << 2)); else advance_pc (4);                             |
| bltzal       | 0b00000100000100000000000000000000 | if $s < 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4);  |
| bne          | 0b00010100000000000000000000000000 | if $s != $t advance_pc (offset << 2)); else advance_pc (4);                           |
| div          | 0b00000000000000000000000000011010 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| divu         | 0b00000000000000000000000000011011 | $LO = $s / $t; $HI = $s % $t; advance_pc (4);                                         |
| j - jump     | 0b00001000000000000000000000000000 | PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);                               |
| jal          | 0b00001100000000000000000000000000 | $31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) &#124; (target << 2);    |
| jr           | 0b00000000000000000000000000001000 | PC = nPC; nPC = $s;                                                                   |
| lb           | 0b10000000000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| lui          | 0b00111100000000000000000000000000 | $t = (imm << 16); advance_pc (4);                                                     |
| lw           | 0b10001100000000000000000000000000 | $t = MEM[$s + offset]; advance_pc (4);                                                |
| mfhi         | 0b00000000000000000000000000010000 | $d = $HI; advance_pc (4);                                                             |
| mflo         | 0b00000000000000000000000000010010 | $d = $LO; advance_pc (4);                                                             |
| mult         | 0b00000000000000000000000000011000 | $LO = $s * $t; advance_pc (4);                                                        |
| multu        | 0b00000000000000000000000000011001 | $LO = $s * $t; advance_pc (4);                                                        |
| noop         | 0b00000000000000000000000000000000 | advance_pc (4);                                                                       |
| or           | 0b00000000000000000000000000100101 | $d = $s &#124; $t; advance_pc (4);                                                    |
| ori          | 0b00110100000000000000000000000000 | $t = $s &#124; imm; advance_pc (4);                                                   |
| sb           | 0b10100000000000000000000000000000 | MEM[$s + offset] = (0xff & $t); advance_pc (4);                                       |
| sll          | 0b00000000000000000000000000000000 | $d = $t << h; advance_pc (4);                                                         |
| sllv         | 0b00000000000000000000000000000100 | $d = $t << $s; advance_pc (4)                                                         |
| slt          | 0b00000000000000000000000000101010 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| slti         | 0b00101000000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltiu        | 0b00101100000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltu         | 0b00000000000000000000000000101011 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| sra          | 0b00000000000000000000000000000011 | $d = $t >> h; advance_pc (4);                                                         |
| srl          | 0b00000000000000000000000000000010 | $d = $t >> h; advance_pc (4);                                                         |
| srlv         | 0b00000000000000000000000000000110 | $d = $t >> $s; advance_pc (4);                                                        |
| sub          | 0b00000000000000000000000000100010 | $d = $s - $t; advance_pc (4);                                                         |
| subu         | 0b00000000000000000000000000100011 | $d = $s - $t; advance_pc (4);                                                         |
| sw           | 0b10101100000000000000000000000000 | MEM[$s + offset] = $t; advance_pc (4);                                                |
| syscall      | 0b00000000000000000000000000001100 | advance_pc (4)                                                                        |
| xor          | 0b00000000000000000000000000100110 | $d = $s ^ $t; advance_pc (4);                                                         |
| xori         | 0b00111000000000000000000000000000 | $t = $s ^ imm; advance_pc (4);                                                        |
****
### Supported System calls:
| Value | Name                          | Description                                                                             |
| ---          | ---                                | ---                                                                                   |
| (1)          | Print integer | Prints an integer held in register $a0=$4.|
| (4)          | Print string  | Prints a null-terminated string, where $a0  points to the string. Note that the string will be stored as consecutive bytes in your memory array (of ints), so you will have to deal with the differences.   
| (5)          | Read integer | Reads an integer from stdin (the keyboard), place it in register $v0=$2.|
| (8)          | Read string | Reads a string into address pointed to by $a0=$4, up to $a1-1 characters, and null terminates the string. Note that the characters must be stored as bytes, so you will have to deal with converting a string from the language used for your simulator to a null terminated string stored in an array of ints.|
| (9)          | Allocate memory | Allocates bytes based on $a0=$4, returns address in $v0=$2|
| (10)          | Exit | Exits the program, stopping the simulator.|
| mult         | 0b00000000000000000000000000011000 | $LO = $s * $t; advance_pc (4);                                                        |
| multu        | 0b00000000000000000000000000011001 | $LO = $s * $t; advance_pc (4);                                                        |
| noop         | 0b00000000000000000000000000000000 | advance_pc (4);                                                                       |
| or           | 0b00000000000000000000000000100101 | $d = $s &#124; $t; advance_pc (4);                                                    |
| ori          | 0b00110100000000000000000000000000 | $t = $s &#124; imm; advance_pc (4);                                                   |
| sb           | 0b10100000000000000000000000000000 | MEM[$s + offset] = (0xff & $t); advance_pc (4);                                       |
| sll          | 0b00000000000000000000000000000000 | $d = $t << h; advance_pc (4);                                                         |
| sllv         | 0b00000000000000000000000000000100 | $d = $t << $s; advance_pc (4)                                                         |
| slt          | 0b00000000000000000000000000101010 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| slti         | 0b00101000000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltiu        | 0b00101100000000000000000000000000 | if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);                      |
| sltu         | 0b00000000000000000000000000101011 | if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);                       |
| sra          | 0b00000000000000000000000000000011 | $d = $t >> h; advance_pc (4);                                                         |
| srl          | 0b00000000000000000000000000000010 | $d = $t >> h; advance_pc (4);                                                         |
| srlv         | 0b00000000000000000000000000000110 | $d = $t >> $s; advance_pc (4);                                                        |
| sub          | 0b00000000000000000000000000100010 | $d = $s - $t; advance_pc (4);                                                         |
| subu         | 0b00000000000000000000000000100011 | $d = $s - $t; advance_pc (4);                                                         |
| sw           | 0b10101100000000000000000000000000 | MEM[$s + offset] = $t; advance_pc (4);                                                |
| syscall      | 0b00000000000000000000000000001100 | advance_pc (4)                                                                        |
| xor          | 0b00000000000000000000000000100110 | $d = $s ^ $t; advance_pc (4);                                                         |
| xori         | 0b00111000000000000000000000000000 | $t = $s ^ imm; advance_pc (4);                                                        |
****
### Supported System calls:
| Value | Name                          | Description                                                                             |
| ---          | ---                                | ---                                                                                   |
| (1)          | Print integer | Prints an integer held in register $a0=$4.|
| (4)          | Print string  | Prints a null-terminated string, where $a0  points to the string. Note that the string will be stored as consecutive bytes in your memory array (of ints), so you will have to deal with the differences.   
| (5)          | Read integer | Reads an integer from stdin (the keyboard), place it in register $v0=$2.|
| (8)          | Read string | Reads a string into address pointed to by $a0=$4, up to $a1-1 characters, and null terminates the string. Note that the characters must be stored as bytes, so you will have to deal with converting a string from the language used for your simulator to a null terminated string stored in an array of ints.|
| (9)          | Allocate memory | Allocates bytes based on $a0=$4, returns address in $v0=$2|
| (10)          | Exit | Exits the program, stopping the simulator.|
