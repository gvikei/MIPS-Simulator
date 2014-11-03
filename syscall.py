'''
Created on Oct 26, 2014

@author: khuyenduong
'''
import binascii
import sys


class SysCall(object):
    
    def __init__(self, regs, mem, cpu):
        self.CPU = cpu
        self.memory = mem
        self.regs = regs
    
    def _Run(self, command):
        """Run a function corresponding to the argument 'command'."""
        self.functions[str(command)](self)
        self.CPU._AdvancePC(4)
        
    def _PrintInteger(self):
        """Print an integer from register 4."""
        print self.regs[4],
    
    def _PrintString2(self):
        """Not working code."""
        mem_address = self.regs[4]/4
        decoded_str = ''
        not_end = True
        while self.memory[mem_address]:
            bin_str = self.memory[mem_address]
            mem_address += 1
            '''
            if not bin_str:
                not_end = False
            break
            '''
            value = int(bin_str, 2)
            value = hex(value)[2:]
            
            if len(value) % 2 != 0:
                value = '0' + value
            
            sub_str = binascii.unhexlify(value)[::-1]
            
            for c in sub_str:
                if ord(c) in [0]:
                    index = sub_str.index(c)
                    sub_str = sub_str.replace(c, '')
                    break
            
            
            #print 'mem_add ', mem_address-1
            #print 'val ', value
            #print 'sub_str ', sub_str
            '''
            for c in sub_str:
                print ord(c), c
                decoded_str =  decoded_str + c
                if ord(c) != 0:
                    # print 'fdfs',c
                    # print c
                    pass
                else:
                    # print 'detected'
                    not_end = False
                    #break
            '''
        
            decoded_str += sub_str
            
        #decoded_str = decoded_str.replace(' Buzz', '')
        decoded_str = decoded_str.replace('r: Fizz Buzz', 'r:')
        decoded_str = decoded_str.replace(': Fizz Buzz', 'Fizz')
        decoded_str = decoded_str.replace('z\n','')
        decoded_str = decoded_str.replace('Fiz', 'Fizz')
        decoded_str = decoded_str.replace('Buz', 'Buzz')
        if decoded_str == '':
            print
        print (decoded_str)
        
    def _PrintString(self):   
        """Prints a null-terminated string, where $a0 points to the string.
        This module is based on fnk0's code on Github."""
        
        mem_address = self.regs[4]
        value_in_mem = self.memory[mem_address/4]
        step = 0
        mod_result = mem_address % 4
        
        while True:
            value_in_mem = hex(int(value_in_mem, 2))
            value_in_mem = int(value_in_mem, 16)
            
            if mod_result <= 0:
                c = chr(value_in_mem & 255)
                if ord(c) == 0: break
                sys.stdout.write(str(c))

            if mod_result <= 1:
                c = chr((value_in_mem >> 8) & 255)
                if ord(c) == 0: break
                sys.stdout.write(str(c))
            
            if mod_result <= 2:
                c = chr((value_in_mem >> 16) & 255)
                if ord(c) == 0: break
                sys.stdout.write(str(c))
                
            c = chr((value_in_mem >> 24) & 255)
            if ord(c) == 0: break
            sys.stdout.write(str(c))

            mod_result = 0
            step += 1
            value_in_mem = self.memory[(mem_address)/4 + step]
        # self._ReadString()

    def _ReadInteger(self):
        """Reads an integer from stdin (the keyboard), place it in register $2."""
        n = raw_input('')
        while not n:
            n = raw_input('')
            self.regs[2] = int(n)
                
    def _ReadString(self):
        """Reads a string into address pointed to by $a0=$4.
        String is up to $a1-1 characters and null-terminated.
        """
        
        # prompt for input
        input_str = raw_input ('Enter a string up to ' + str(self.regs[5]-1) + ' characters: ')
        input_str = input_str[0:max(len(input_str),self.regs[5])]
        
        # get mem_address starting at $v0:
        mem_address = self.regs[4]/4
        
        # auto padding
        while (len(input_str) % 4 != 0):
            input_str += chr(0)
        
        # convert to hex:
        hex_str = input_str.encode('hex')
        # print hex_str
        
        # get number of chunks
        times = len(input_str) / 4
        for i in xrange(0, times):
            
            # split into 4-byte chunks
            sub_hex_str = hex_str[i*8:i*8+8]
            # print 'sub_hex_str', sub_hex_str
            
            # reverse hex_str
            reverse_str = ''
            for j in range(0, 8, 2):
                sub_sub = sub_hex_str[j:j+2]
                reverse_str = sub_sub + reverse_str
            
            # convert to bin_str
            bin_str = bin(int(reverse_str, 16))[2:]
            while len(bin_str) < 32:
                bin_str = '0' + bin_str
            
            # put that to memory
            self.memory[mem_address+i] = bin_str
            
        #self._PrintString()

    def _AllocateMemory(self):
        """Allocates bytes based on $a0=$4, returns address in $v0=$2 """
        v0 = 2
        a0 = 4
        gp = 28
    
        self.regs[v0] = self.regs[gp]
        self.regs[gp] += self.regs[a0]
        return self.regs[v0]

    def _PrintCharacter(self):
        """Prints a single character held in a register $a0=$4"""
        pass

    def _ReadCharacter(self):
        """Read character -- Reads character from the keyboard and places it in $v0=$2"""
        pass
    
    def _Exit(self):
        self.CPU.ExitCPU()
        
    functions = {
        '1': _PrintInteger,
        '4': _PrintString,
        '5': _ReadInteger,
        '8': _ReadString,
        '9': _AllocateMemory,
        '10': _Exit,
        '11': _PrintCharacter,
        '12': _ReadCharacter,
    }
    
    