"""Logs:

Created on Oct 19, 2014

@author: khuyenduong

----------------------
Oct 20, 0:44 AM

- Ignore TypeError, b/c it caused by running every single unit test and no params were given
- Basically everything works
- 'syscall' confused with 'and'

Oct 20, 19:20 PM
- Found a bug in test count.txt:
    e.g: [0x0000005c]    0x25080001  addi $8, $8, 1 
    explanation: addi should be addiu
    
- added funct matching when opcode is duplicated, working so far

Oct 25, 17:53 PM
- Finished all the val functions, except for syscall
- Implemented putting value into mem, not sure right
- Can basically read instruction & run right now

To do:
    syscall
    read stackpointer, PC address from input

Nov 02, 15:22 PM
- Program is finished with (seemingly) no bugs in Normal mode.
- Debug mode has bugs when user input required. 
  Can bypass by repeatedly enter same input until PC and Instr are printed
- Needs code review

----------------------
"""
import unittest
import parser

import cpu
import execute


class Test(unittest.TestCase):
    
    def setUp(self):
        self.CPU = cpu.CPU()
        self.memory = self.CPU.memory
        self.registers = self.CPU.registers
        self.exe = execute.Executer(self.registers, self.memory, self.CPU)

    def test_get_instruction(self, hex_instr):  
        
        # input
        my_parser = parser.LineParser()
        parsing_result = my_parser.Parse(hex_instr)
        
        if parsing_result is not None:
            line_type, parsed_data = parsing_result
            if line_type == 0: # normal instruction
                
                # put values to memory
                mem, instr = parsed_data
                print "mem, instr", mem, instr
                counter = 0
                for sub_str in instr:
                    self.memory[(mem + counter)/4] = sub_str
                    counter += 4
        
            elif line_type == 1: # pc
                starting_address = parsed_data[0]
                self.CPU.CODE_STARTING_ADDRESS = starting_address / 4
                print self.CPU.CODE_STARTING_ADDRESS
                
            elif line_type == 2: # r
                register, value = parsed_data[0], parsed_data[1]
                self.registers[register] = value / 4 
                print register, value, self.registers[register]
    
    def test_run_instruction(self, parsed_instr):
        print parsed_instr
        
        try:
            for line in parsed_instr:
                mem_address = line['mem']
                self.memory[mem_address/4] = line['instr']
                self.registers = self.exe.eval(line)
                print self.registers, line
                print

        except TypeError:
            pass
        
    def test_all(self):
        file_name = 'mips_hex.txt'
        test_data = open(file_name, 'r').readlines()
        for line in test_data:
            self.test_get_instruction(line)

if __name__ == "__main__":
    unittest.main()
