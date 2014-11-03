'''
Created on Oct 23, 2014

@author: khuyenduong
'''
import execute
import parser
import instruction
import sys
import syscall

class CPU(object):
    
    MEMORY_SIZE_IN_BYTES  = (1 << 20) * 4
    CODE_STARTING_ADDRESS = 0
    DATA_STARTING_ADRESS = 1 << 16
    STACK_STARTING_ADDRESS = MEMORY_SIZE_IN_BYTES - 4
    NUMBER_OF_REGISTERS = 32
    
    def __init__(self):
        
        # registers declare
        self.registers = [0] * self.NUMBER_OF_REGISTERS
        self.PC = self.CODE_STARTING_ADDRESS;
        self.nPC = self.CODE_STARTING_ADDRESS;
        self.HI = None
        self.LO = None
        
        # memory declare
        self.memory = [0] * self.MEMORY_SIZE_IN_BYTES
        
        # register init
        self.registers[29] = self.STACK_STARTING_ADDRESS
        self.registers[0] = 0
        
        # for debug mode
        self.current_line = None
        
        # saying Hi
        print '----------------------------------------------------------'
        print '        MIPS Simulator Program by Khuyen Duong'
        print '----------------------------------------------------------'

        
    def _LoadInstructions(self, file_name):
        
        # read data from file
        test_data = open(file_name, 'r').readlines()
        for line in test_data:
            self._GetInstruction(line)
            
    def _AdvancePC(self, offset):
        self.PC = self.nPC
        self.nPC += offset
        # print 'PC, nPC: ', self.PC, self.nPC
        return self.PC, self.nPC
        
    def _GetInstruction(self, hex_instr):
        
        # input
        my_parser = parser.LineParser()
        parsing_result = my_parser.Parse(hex_instr)
        
        if parsing_result is not None:
            line_type, parsed_data = parsing_result
            if line_type == 0: # normal instruction
                
                # put values to memory
                mem, instr = parsed_data
                # print "mem, instr", mem, instr
                counter = 0
                for sub_str in instr:
                    self.memory[(mem + counter)/4] = sub_str
                    # print sub_str, " was put into: ", (mem+counter)/4
                    counter += 4
        
            elif line_type == 1: # pc
                starting_address = parsed_data[0]
                self.CODE_STARTING_ADDRESS = starting_address / 4
                # print 'code_starting_address ', self.CODE_STARTING_ADDRESS
                
            elif line_type == 2: # r
                register, value = parsed_data[0], parsed_data[1]
                self.registers[register] = value / 4 
                # print register, value, self.registers[register]
            
    def _BinaryToExecutable(self, sub_instr):
                        
        # init
        data = []
        data_line = {}
    
        # get opcode
        try:    
            # init
            opcode = sub_instr[:6]
            opcodes = instruction.opcodes
            
            # get function according to opcode
            function = opcodes.keys()[opcodes.values().index(opcode)]
            
            # get instruction type (I, R, J)
            instruction_type = -1
            for instruction_list in instruction.instructions:
                if function in instruction_list:
                    instruction_type = instruction.instructions.index(instruction_list)
                    # print 'instruction type: ', instruction_type
                    break
            
            # if opcode is duplicate, get funct info and match  
            
            # 1. check if opcode was duplicated:
            counter = 0
            dup_found = False
            for key, value in opcodes.items():
                if (value == opcode):
                    counter +=1
            # duplicates found
            if counter > 1: 
                dup_found = True       
            
            # 2. get match of funct if opcode was duplicated  
            funct = sub_instr[26:32]
            functs = instruction.functs
            # print funct,
            if dup_found:
                function = functs.keys()[functs.values().index(funct)]
            
            # print all the properties
            decoded_instr = instruction.Decode(sub_instr, instruction_type)
            properties = (vars(decoded_instr))
            
            
            # get real data_line
            data_line['operation'] = function
            
            # print 'instruction: ', function
            for prop in properties:
                bin_value = (properties[prop])
                dec_value = int(bin_value, 2)
                # print prop, dec_value,
                data_line[prop] = dec_value
                
            data.append(data_line)
            
        except TypeError:
            # print "Unexpected error:", sys.exc_info()[0]
            sys.exit()
        
        return data_line
    
    def ExecuteInstruction(self, data_line):
        
        # init the executer
        exe = execute.Executer(self.registers, self.memory, self)
        
        # executing a line
        self.registers = exe.eval(data_line)
        
    def ExecuteCPU(self):
        while True:
            self.RunOnce()
            
    def RunOnce(self):
        line = self.memory[self.PC/4]
        try:
            #print 'instruction in bin: ', line
            #print "PC: ", self.PC/4
            #print "instruction from memory: ", hex(int(line,2))
            
            # parse
            data_line = self._BinaryToExecutable(line)
            # for debug mode
            self.current_line = data_line
            #print 'data_line: ', data_line
            self.ExecuteInstruction(data_line)
            
            # for debugging
            #print
            #print self.registers
            #print
        
        except TypeError:
            # print "Unexpected error:", sys.exc_info()[0]
            pass
        
        except KeyError:
            # print "Unexpected error:", sys.exc_info()[0]
            pass
    
    
    def ExitCPU(self):
        sys.exit(0)
        
    def PrintRegisters(self, base):
        if base == 2:
            for i in xrange(0, len(self.registers)):
                sys.stdout.write('[' + str(i+1) + ']: ' + bin(self.registers[i])[2:] + '\n')
        elif base == 10:
            for i in xrange(0, len(self.registers)):
                sys.stdout.write('[' + str(i+1) + ']: ' + str(self.registers[i]) + '\n')
        elif base == 16:
            for i in xrange(0, len(self.registers)):
                sys.stdout.write('[' + str(i+1) + ']: ' + hex(self.registers[i])[2:] + '\n')

