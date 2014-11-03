opcodes = {
    'add':'000000' , 'addu':'000000' , 'and':'000000' , 'break':'000000' , 'div':'000000' , 'divu':'000000' ,
    'jalr':'000000' , 'jr':'000000', 'mfhi':'000000' , 'mflo':'000000' , 'mthi':'000000' , 'mtlo':'000000' ,
    'mult':'000000' , 'multu':'000000' , 'nor':'000000' , 'or':'000000' , 'sll':'000000' , 'sllv':'000000' ,
    'slt':'000000' , 'sltu':'000000' , 'sra':'000000' , 'srav':'000000' , 'srl':'000000' ,'srlv':'000000' ,
    'sub':'000000' , 'subu':'000000' , 'syscall':'000000' , 'xor':'000000' , 'rfe':'000000',

    'addi':'001000' , 'addiu':'001001' , 'andi':'001100' , 'beq':'000100' , 'bgez':'000001' , 'bgtz':'000111' ,
    'blez':'000110' , 'bltz':'000001', 'bne':'000101' , 'lb':'100000' , 'lbu':'100100' , 'lh':'100001' ,
    'lhu':'100101' , 'lui':'001111' , 'lw':'100011' , 'lwc1':'110001' , 'ori':'001101' , 'sb':'101000' ,
    'slti':'001010' , 'sltiu':'001011' , 'sh':'101001' , 'sw':'101011' , 'swc1':'111001' , 'xori':'001110' ,

    'j':'000010' , 'jal':'000011' ,
}

functs = {
    'add':'100000' , 'addu':'100001' , 'and':'100100' , 'break':'001101' , 'div':'011010' , 'divu':'011011' ,
    'jalr':'001001' , 'jr':'001000', 'mfhi':'010000' , 'mflo':'010010' , 'mthi':'010001' , 'mtlo':'010011' ,
    'mult':'011000' , 'multu':'011001' , 'nor':'100111' , 'or':'100101' , 'sll':'000000' ,
    'sllv':'000100' , 'slt':'101010' , 'sltu':'101011' , 'sra':'000011' , 'srav':'000111' , 'srl':'000010' ,
    'srlv':'000110' , 'sub':'100010' , 'subu':'100011' , 'syscall':'001100' , 'xor':'100110' , 'rfe':'010000' ,
}

forms = {
    'cvt.s.w':'10100' , 'cvt.w.s':'10000' , 'mfc0':'00000' , 'mfc1':'00000' , 'mtc0':'00100' , 'mtc1':'00100' ,
    'bc1t':'01000' ,  'bc1f':'01000' , 'bc1tl':'01000' , 'bc1fl':'01000'
}

I_instructions = ['addi', 'addiu', 'andi', 'beq', 'bne', 'lbu', 
                  'lhu', 'lui', 'lw', 'ori', 'sb', 'sh', 'slti', 'sltiu', 'sw']

R_instructions = ['add', 'addu', 'and', 'div', 'divu', 'jr', 
                  'mfhi', 'mflo', 'mult', 'multu', 'nor', 'xor', 'or',
                  'slt', 'sltu', 'sll', 'srl', 'sra', 'sub', 'subu']

J_instructions = ['jal', 'j']

instructions = [I_instructions, R_instructions, J_instructions]

reg_names=['zero', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7',
             's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 't8', 't9', 'k0', 'k1', 'gp', 'sp', 'fp', 'ra']

def Decode(instr_bin, instr_type):
    """Get the member info (s, t, d...) of a binary instruction based on its type."""
    decoded_instr = None
    if instr_type == 0:
        decoded_instr = IInstruction(instr_bin)
    elif instr_type == 1:
        decoded_instr = RInstruction(instr_bin)
    else:
        decoded_instr = JInstruction(instr_bin)
    return decoded_instr

class Instruction(object):
    """
        Type 0: I, 1: R, 2: J 
        R-instruction: opcode    rs    rt        rd        shift (shamt)    funct
                       0-5       6-10  11-15    16-20        21-25          26-31
        I-instruction: opcode    rs    rt        IMM
                       0-5       6-10  11-15    16-31
        J-instruction: opcode    address
                       0-5       6-31 
    """
    def get_s(self):
        return self.instr[6:11]
    
    def get_t(self):
        return self.instr[11:16]
    
    def get_d(self):
        return self.instr[16:21]
    
    def get_i(self):
        return self.instr[16:32]
    
    def get_shift(self):
        return self.instr[21:26]
    
    def get_funct(self):
        return self.instr[26:32]
    
    def get_address(self):
        return self.instr[6:32]
    
    def __init__(self, instr):
        self.instr = instr

class RInstruction(Instruction):
    def __init__(self, r_instr):
        self.instr = r_instr
        self.s = self.get_s()
        self.t = self.get_t()
        self.d = self.get_d()  
        self.shift = self.get_shift()
        self.funct = self.get_funct()
        
class IInstruction(Instruction):
    def __init__(self, i_instr):
        self.instr = i_instr
        self.s = self.get_s()
        self.t = self.get_t()
        self.i = self.get_i()
        
class JInstruction(Instruction):
    def __init__(self, j_instr):
        self.instr = j_instr
        self.address = self.get_address()