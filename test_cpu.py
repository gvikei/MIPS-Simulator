'''
Created on Oct 26, 2014

@author: khuyenduong
'''
import cpu

def main():
    CPU = cpu.CPU()
    CPU._LoadInstructions('count.txt')
    CPU.ExecuteCPU()

if __name__ == "__main__":
    main()