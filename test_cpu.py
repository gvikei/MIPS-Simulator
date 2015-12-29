'''
Created on Oct 26, 2014
Updated on Dec 29, 2015

@author: khuyenduong

How to run: python test_cpu.py [instruction_file]
E.g.: python test_cpu.py fizzbuzz.txt
'''
import cpu, sys, os

def file_input():
    if (len(sys.argv) < 2):
        print "Please add file name to the argument as the following:"
        print "python test_cpu.py [instruction_file]"
        print "E.g.: python test_cpu.py testFiles/fizzbuzz.txt"
        sys.exit()

    instruction_file = sys.argv[1]
    while (not os.path.isfile(instruction_file)):
        instruction_file = raw_input("File name was invalid. Please try another one: ")
            
    return instruction_file

if __name__ == "__main__":
    # reading and executing instruction file
    CPU = cpu.CPU()
    CPU._LoadInstructions(file_input())
    CPU.ExecuteCPU()
