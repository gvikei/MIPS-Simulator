'''
Created on Nov 2, 2014

@author: khuyenduong
'''

import cpu
import sys

FILE_NAME = 'fizzBuzz.txt'
DEBUG_MODE = False

def print_usage_instr():
    print 'usage: MIPS -d [file]    --> run instructions in [file] in DEBUG mode'
    print '   or: MIPS -n [file]    --> run instructions in [file] in NORMAL mode'
    sys.exit()

def prompt():
    global DEBUG_MODE
    
    # in case wrong args
    if len(sys.argv) != 3:
        print_usage_instr()
        
    
    # check mode:
    if sys.argv[1] == '-d':
        DEBUG_MODE = True
    elif sys.argv[1] == '-n':
        DEBUG_MODE = False
    else:
        print_usage_instr()
        
    # get file name
    global FILE_NAME 
    FILE_NAME = sys.argv[2]
    
def print_debug_instr():
    print 'Debug mode is ON. Available debugging commands: '
    print '"Enter" key              | Execute current line'
    print '-m -[location in hex]    | Print value stored at [location] in memory'
    print '-r -hex                  | Print contents of registers in hexadecimal'
    print '-r -dec                  | Print contents of registers in decimal'
    print '-r -bin                  | Print contents of registers in binary'
        
def main():
    # load CPU
    CPU = cpu.CPU()
    
    # prompt stuff
    prompt()
    
    # prepare to run
    CPU._LoadInstructions(FILE_NAME)
    
    # DEBUG_MODE = True
    
    if DEBUG_MODE:
        
        # print debug instruction
        print_debug_instr()
        
        while True:
            # get input
            cmd = raw_input('')
            
            # split input
            args = cmd.split(' ')
            
            # hopefully right input entered
            if len(args) == 2:
                
                # print mem
                if args[0] == '-m':
                    
                    # get value
                    mem_addr = int(args[1], 16)
                    mem_addr = mem_addr/4
                    
                    # print out
                    try:
                        print 'Value at', mem_addr, ': ', hex(int(CPU.memory[mem_addr], 2))
                    except:
                        print 'Wrong location entered'
                
                # print register
                if args[0] == '-r':
                    
                    # get type of value to print out
                    if args[1] == '-hex':
                        CPU.PrintRegisters(16)
                        
                    if args[1] == '-dec':
                        CPU.PrintRegisters(10)
                        
                    if args[1] == '-bin':
                        CPU.PrintRegisters(2)
            else:
                # execute 1 line
                CPU.RunOnce()
                # print PC and current instruction
                print 'PC:', CPU.PC
                print 'Instruction:', hex(CPU.current_line['instr'])
    else:
        CPU.ExecuteCPU()     
           
if __name__ == "__main__":
    main()