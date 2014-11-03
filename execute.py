import syscall

class Executer(object):
    
    def __init__(self, regs, mem, cpu):
        self.regs = regs
        self.mem = mem
        self.CPU = cpu
        self.syscall = syscall.SysCall(regs, mem, cpu)
    
    def eval(self, instr):
        self.instructions[instr['operation']](self, instr)
        return self.regs
    
    def _add(self, f): #$d = $s + $t; advance_pc (4);
        d, s, t = f['d'], f['s'], f['t']
        self.regs[d] = self.regs[s] + self.regs[t]
        self.CPU._AdvancePC(4)
        
    def _addi(self, f): # $t = $s + imm; advance_pc (4);
        t, s, i = f['t'], f['s'], f['i']
        self.regs[t] = self.regs[s] + i
        self.CPU._AdvancePC(4)

    def _addu(self, f): #$d = $s + $t; advance_pc (4)
        self._add(f)

    def _addiu(self, f): #$t = $s + imm; advance_pc (4);
        t, s, i = f['t'], f['s'], f['i']
        self.regs[t] = self.regs[s] + i
        self.CPU._AdvancePC(4)

    def _and(self, f): #$d = $s & $t; advance_pc (4);
        d, s, t = f['d'], f['s'], f['t']
        self.regs[d] = self.regs[s] & self.regs[t]
        self.CPU._AdvancePC(4)

    def _andi(self, f): #$t = $s & imm; advance_pc (4);
        t, s, i = f['t'], f['s'], f['i']
        self.regs[t] = self.regs[s] & i
        self.CPU._AdvancePC(4)

    def _beq(self, f): # if $s == $t advance_pc (offset << 2)); else advance_pc (4);
        # print 'PC before branching: ', self.CPU.PC
        s, t, i = f['s'], f['t'], f['i']
        if self.regs[s] == self.regs[t]:
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)
            # print 'after loop: ', hex(self.CPU.PC), 'val at: ', self.CPU.PC, ' is: ', self.mem[self.CPU.PC/4]
            
    def _bgez(self, f): # if $s >= 0 advance_pc (offset << 2)); else advance_pc (4);
        s, i = f['s'], f['i']
        if self.regs[s] >= 0:
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)

    def _bgezal(self, f): #if $s >= 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4);
        s, i = f['s'], f['i']
        if self.regs[s] >= 0:
            self.regs[31] = self.CPU.nPC + 4
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)

    def _bgtz(self, f): #if $s > 0 advance_pc (offset << 2)); else advance_pc (4);
        s, i = f['s'], f['i']
        if self.regs[s] > 0:
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)

    def _blez(self, f): #if $s <= 0 advance_pc (offset << 2)); else advance_pc (4)
        s, i = f['s'], f['i']
        if self.regs[s] <= 0:
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)
            
    def _bltz(self, f): #if $s < 0 advance_pc (offset << 2)); else advance_pc (4);
        s, i = f['s'], f['i']
        if self.regs[s] < 0:
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)
            
    def _bltzal(self, f): #if $s < 0 $31 = PC + 8 (or nPC + 4); advance_pc (offset << 2)); else advance_pc (4);
        s, i = f['s'], f['i']
        if self.regs[s] < 0:
            self.regs[31] = self.CPU.nPC + 4
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)

    def _bne(self, f): # if $s != $t advance_pc (offset << 2)); else advance_pc (4);
        s, t, i = f['s'], f['t'], f['i']
        if self.regs[s] != self.regs[t]:
            self.CPU.PC, self.CPU.nPC = self.CPU._AdvancePC(i << 2)
        else:
            self.CPU._AdvancePC(4)
        
    def _div(self, f): #$LO = $s / $t; $HI = $s % $t; advance_pc (4);
        s, t = f['s'], f['t']
        self.CPU.LO = self.regs[s]/self.regs[t]
        self.CPU.HI = self.regs[s]%self.regs[t]
        self.CPU._AdvancePC(4)
        # print self.regs[s],"/",self.regs[t]," = ",self.CPU.LO,self.regs[s],"%",self.regs[t]," = ",self.CPU.HI
        

    def _divu(self, f):     #$LO = $s / $t; $HI = $s % $t; advance_pc (4);
        self._div(f)

    def _j(self, f): #PC = nPC; nPC = (PC & 0xf0000000) | (target << 2);
        i = f['address']
        #print 'PC and nPC before: ', self.CPU.PC/4, self.CPU.nPC/4
        self.CPU.PC = self.CPU.nPC  
        self.CPU.nPC = (self.CPU.PC & 0xf0000000) | (i << 2)
        #print 'PC and nPC after: ', self.CPU.PC/4, self.CPU.nPC/4
        #print

    def _jal(self, f): #$31 = PC + 8 (or nPC + 4); PC = nPC; nPC = (PC & 0xf0000000) | (target << 2);
        i = f['address']
        # print 'PC and nPC before: ', self.CPU.PC, self.CPU.nPC
        #print 'PC and nPC before: ', self.CPU.PC/4, self.CPU.nPC/4
        self.regs[31] = self.CPU.nPC + 4
        self.CPU.PC = self.CPU.nPC
        self.CPU.nPC = (self.CPU.PC & 0xf0000000) | (i << 2)
        #print 'PC and nPC after: ', self.CPU.PC/4, self.CPU.nPC/4
        # print 'PC and nPC after: ', self.CPU.PC, self.CPU.nPC

    def _jr(self, f): #PC = nPC; nPC = $s;
        s = f['s']
        self.CPU.PC = self.CPU.nPC
        self.CPU.nPC = self.regs[s]

    def _lb(self, f):     #$t = MEM[$s + offset]; advance_pc (4);
        s, t, i = f['s'], f['t'], f['i']
        self.regs[t] = (self.mem[((self.regs[s] & 0xff) + i)/4])
        self.CPU._AdvancePC(4)

    def _lui(self, f):     #$t = (imm << 16); advance_pc (4);
        t, i = f['t'], f['i']
        self.regs[t] = i << 16
        self.CPU._AdvancePC(4)

    def _lw(self, f):     #$t = MEM[$s + offset]; advance_pc (4);
        t, s, i = f['t'], f['s'], f['i']
        self.regs[t] = self.mem[(self.regs[s] + i)/4]
        self.CPU._AdvancePC(4)

    def _mfhi(self, f): #$d = $HI; advance_pc (4);
        d = f['d']
        self.regs[d] = self.CPU.HI
        self.CPU._AdvancePC(4)

    def _mflo(self, f): #$d = $LO; advance_pc (4);
        d = f['d']
        self.regs[d] = self.CPU.LO
        self.CPU._AdvancePC(4)

    def _mult(self, f): # $LO = $s * $t; advance_pc (4);
        s, t = f['s'], f['t']
        self.CPU.LO = self.regs[s] * self.regs[t]
        self.CPU._AdvancePC(4)

    def _multu(self, f):
        self._mult(f)

    def _nop(self):
        self.CPU._AdvancePC(4)
        
    def _or(self, f): #$d = $s | $t; advance_pc (4);
        d, s, t = f['d'], f['s'], f['t']
        self.regs[d] = self.regs[s] | self.regs[t]
        self.CPU._AdvancePC(4)

    def _ori(self, f): #$t = $s | imm; advance_pc (4);
        t, s, i = f['t'], f['s'], f['i']
        self.regs[t] = self.regs[s] | i
        self.CPU._AdvancePC(4)
        
    def _sb(self, f): #MEM[$s + offset] = (0xff & $t); advance_pc (4);
        s, i, t = f['s'], f['i'], f['t']
        self.mem[(self.regs[s] + i)] = 0xff & self.regs[t]
        self.CPU._AdvancePC(4)
        # print (self.regs[s] + i) / 4, self.mem[(self.regs[s] + i) / 4]

    def _sll(self, f): #$d = $t << h; advance_pc (4);
        t, d, shift = f['t'], f['d'], f['shift']
        self.regs[d] = self.regs[t] << shift
        self.CPU._AdvancePC(4)
        # print self.regs[d], self.regs[t]

    def _sllv(self, f): #$d = $t << $s; advance_pc (4);
        s, t, d = f['s'], f['t'], f['d']
        self.regs[d] = self.regs[t] << self.regs[s]
        self.CPU._AdvancePC(4)

    def _slt(self, f): #if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);
        s, t, d = f['s'], f['t'], f['d']
        if self.regs[s] < self.regs[t]:
            self.regs[d] = 1
        else:
            self.regs[d] = 0
        self.CPU._AdvancePC(4)

    def _slti(self, f): #if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);
        s, t, i = f['s'], f['t'], f['i']
        if self.regs[s] < i:
            self.regs[t] = 1
        else:
            self.regs[t] = 0
        self.CPU._AdvancePC(4)

    def _sltiu(self, f): #if $s < imm $t = 1; advance_pc (4); else $t = 0; advance_pc (4);
        self._slti(f)
        
    def _sltu(self, f): #if $s < $t $d = 1; advance_pc (4); else $d = 0; advance_pc (4);
        self._slt(f)

    def _sra(self, f): #$d = $t >> h; advance_pc (4);
        t, d, shift = f['t'], f['d'], f['shift']
        self.regs[d] = self.regs[t] >> shift
        self.CPU._AdvancePC(4)

    def _srl(self, f): #$d = $t >> h; advance_pc (4);
        self._sra(f)

    def _srlv(self, f): #$d = $t >> $s; advance_pc (4);
        d, t, s = f['d'], f['t'], f['s']
        self.regs[d] = self.regs[t] >> self.regs[s]
        self.CPU._AdvancePC(4)

    def _sub(self, f): #$d = $s - $t; advance_pc (4);
        d, t, s = f['d'], f['t'], f['s']
        self.regs[d] = self.regs[s] - self.regs[t]
        self.CPU._AdvancePC(4)

    def _subu(self, f): #$d = $s - $t; advance_pc (4);
        self._sub(f)

    def _sw(self, f): #MEM[$s + offset] = $t; advance_pc (4);
        s, i, t = f['s'], f['i'], f['t']
        self.mem[(self.regs[s] + i) / 4] = t
        self.CPU._AdvancePC(4)

    def _xor(self, f): #$d = $s ^ $t; advance_pc (4);
        d, t, s = f['d'], f['t'], f['s']
        self.regs[d] = self.regs[s] ^ self.regs[t]
        self.CPU._AdvancePC(4)

    def _xori(self, f): #$t = $s ^ imm; advance_pc (4);
        i, t, s = f['i'], f['t'], f['s']
        self.regs[t] = self.regs[s] ^ i
        self.CPU._AdvancePC(4)

    def _syscall(self, f):
        self.syscall._Run(self.regs[2])
        
    def sign_extend(self, i):
        bin_rep = bin(i)[2:]
        while len(bin_rep) < 16:
            bin_rep = '0' + bin_rep
        
        while len(bin_rep) < 32:
            bin_rep = bin_rep[15] + bin_rep   
            
        decimal = int(bin_rep, 10)
        return decimal
    
    
    instructions = {
        'add': _add,
        'addi': _addi,
        'addiu': _addiu,
        'addu': _addu,
        'and': _and,
        'andi': _andi,
        'beq': _beq,
        'bgez': _bgez,
        'bgezal': _bgezal,
        'bgtz': _bgtz,
        'blez': _blez,
        'bltz': _bltz,
        'bltzal': _bltzal,
        'bne': _bne,
        'div': _div,
        'divu': _divu,
        'j': _j,
        'jal': _jal,
        'jr': _jr,
        'lb': _lb,
        'lui': _lui,
        'lw': _lw,
        'mfhi': _mfhi,
        'mflo': _mflo,
        'mult': _mult,
        'multu': _multu,
        'or': _or,
        'ori': _ori,
        'sb': _sb,
        'sll': _sll,
        'sllv': _sllv,
        'slt': _slt,
        'slti': _slti,
        'sltiu': _sltiu,
        'sltu': _sltu,
        'sra': _sra,
        'srl': _srl,
        'srlv': _srlv,
        'sub': _sub,
        'subu': _subu,
        'sw': _sw,
        'xor': _xor,
        'xori': _xori,
        'syscall': _syscall,
    }
    