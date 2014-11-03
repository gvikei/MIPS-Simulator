import re

class LineParser(object):
    
    def PreProcess(self, raw_line):
        """Strim redundancies of a line from the input."""
        raw_line = raw_line.rstrip()
        raw_line = re.sub(' +', '\t', raw_line)
        raw_line = re.sub('\t+', '\t', raw_line)
        return raw_line
    
    def ParseMemAndInstruction(self, processed_line):
        """Get the hex values of mem and instructions in a line."""
        
        # Split values by tabs
        all_value = processed_line.split("\t")
        
        # Get the mem value
        hex_mem = all_value[0]
        hex_mem = hex_mem [3:len(hex_mem)-1] 
        
        # Get all the instructions
        hex_instr = all_value[1:]
        
        # Pre-process to get only values after 0x
        for item in hex_instr:
            if item[0:2] != '0x':
                hex_instr.remove(item)
        
        return hex_mem, hex_instr
    
    def GetDecimalMemAddress(self, hex_mem):
        """ Get decimal value of mem from hex value"""
    
        decimal_value = long(hex_mem, 16)
        mem_address = decimal_value
        return mem_address
    
    def GetBinaryInstruction(self, hex_instr):
        bin_instr = []
        for instr in hex_instr:
            if instr[0:2] == '0x':
                instr = instr[2:]
                bin_instr.append(bin(long(instr, 16))[2:])
            
        return bin_instr
    
    def ParseRegisterAndValue(self, processed_line):
        """ Return decimal value of register name and the value assigned to it"""
        
        # Split values by tabs
        all_value = processed_line.split('\t')
        
        # Get the register value
        register = all_value[0]
        register = int(register [2:len(register)-1])
        
        # Get the value assigned to the register 
        value = all_value[1:]
        for item in value:
            if (not item.startswith('0x')):
                all_value.remove(item)
            else:
                value = item[2:]
                break
        
        value = int(value, 16)
        return register, value
    
    
    def ParsePCAndMem(self, processed_line):
        # Split values by tabs
        all_value = processed_line.split('\t')
        
        mem = all_value[1:]
        #print 'mem before: ', all_value
        for item in mem:
            #print 'item: ', item
            if item.startswith('0x'):
                mem = item[2:]
                break
 
        mem = int(mem, 16)
        return mem

    def Parse(self, raw_line):
        """ Parse a line from raw input to MIPS instruction
            [0x........] 0x........ ---> 9 ['00110100000000100000000000000100', '01....', '01.....']
        """
        # init
        processed_line = self.PreProcess(raw_line)
        
        if processed_line.startswith('[0x'):
            hex_mem, hex_instr = self.ParseMemAndInstruction(processed_line)
            
            # for debugging
            # print hex_mem, hex_instr
            
            # getting info
            mem_address = self.GetDecimalMemAddress(hex_mem)
            bin_instr = self.GetBinaryInstruction(hex_instr)
            
            # formatting binary instruction
            index = 0
            for instr in bin_instr:
                tmp = instr
                if tmp:
                    bin_instr.remove(instr)
                    while (len(tmp) < 32):
                        tmp = '0' + tmp
                    bin_instr.insert(index, tmp)
                    index += 1
            
            # add values back to object
            self.mem_address = mem_address
            self.bin_instr = bin_instr
            
            result = []
            result.append(mem_address)
            result.append(bin_instr)
            return 0, result
        
        elif processed_line.startswith('[PC]'):
            starting_address = self.ParsePCAndMem(processed_line)
            result = []
            result.append(starting_address)
            return 1, result
        
        elif processed_line.startswith('[R'):
            register, value = self.ParseRegisterAndValue(processed_line)
            result = []
            result.append(register)
            result.append(value)
            return 2, result
        else:
            return None