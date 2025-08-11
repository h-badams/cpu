# TODO: comment

import numpy as np

instruction_table = {}

def register_instr(name):
    def decorator(func):
        instruction_table[name] = func
        return func
    return decorator

# R type instructions

@register_instr('add')
def instr_add(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] + state['registers'][rs2]
    
@register_instr('sub')
def instr_sub(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] - state['registers'][rs2]
    
@register_instr('xor')
def instr_xor(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] ^ state['registers'][rs2]
    
@register_instr('or')
def instr_or(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] | state['registers'][rs2]

@register_instr('and')
def instr_and(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] & state['registers'][rs2]
    
@register_instr('sll')
def instr_sll(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] << state['registers'][rs2]
    
@register_instr('srl')
def instr_srl(args, state):
    rd, rs1, rs2 = args
    state['registers'][rd] = state['registers'][rs1] >> state['registers'][rs2]
    
# TODO: sra instruction

@register_instr('slt')
def instr_slt(args, state):
    rd, rs1, rs2 = args
    slt = signed(state['registers'][rs1]) < signed(state['registers'][rs2])
    if slt:
        state['registers'][rd] = 1
    else:
        state['registers'][rd] = 0
        
@register_instr('sltu')
def instr_sltu(args, state):
    rd, rs1, rs2 = args
    sltu = state['registers'][rs1] < state['registers'][rs2]
    if sltu:
        state['registers'][rd] = 1
    else:
        state['registers'][rd] = 0
        
# I type instructions

@register_instr('addi')
def instr_addi(args, state):
    rd, rs1, imm = args
    state['registers'][rd] = state['registers'][rs1] + imm
    
@register_instr('xori')
def instr_xori(args, state):
    rd, rs1, imm = args
    state['registers'][rd] = state['registers'][rs1] ^ imm
    
@register_instr('ori')
def instr_ori(args, state):
    rd, rs1, imm = args
    state['registers'][rd] = state['registers'][rs1] | imm
    
@register_instr('andi')
def instr_andi(args, state):
    rd, rs1, imm = args
    state['registers'][rd] = state['registers'][rs1] & imm
    
@register_instr('slli')
def instr_slli(args, state):
    rd, rs1, imm = args
    state['registers'][rd] = state['registers'][rs1] << imm
    
@register_instr('srli')
def instr_srli(args, state):
    rd, rs1, imm = args
    state['registers'][rd] = state['registers'][rs1] >> imm
    
# TODO: srai instruction

@register_instr('slti')
def instr_slti(args, state):
    rd, rs1, imm = args
    slti = signed(state['registers'][rs1]) < signed(imm)
    if slti:
        state['registers'][rd] = 1
    else:
        state['registers'][rd] = 0
        
@register_instr('sltiu')
def instr_sltiu(args, state):
    rd, rs1, imm = args
    sltiu = state['registers'][rs1] < imm
    if sltiu:
        state['registers'][rd] = 1
    else:
        state['registers'][rd] = 0
        
@register_instr('lb')
def instr_lb(args, state):
    rd, rs1, imm = args
    addr = state['registers'][rs1] + imm
    state['registers'][rd] = sign_ext(state['memory'][addr], 8)

@register_instr('lh')
def instr_lh(args, state):
    rd, rs1, imm = args
    addr = state['registers'][rs1] + imm
    halfword = state['memory'][addr:addr+2].view('<u2')[0]
    state['registers'][rd] = sign_ext(halfword, 16)
    
@register_instr('lw')
def instr_lw(args, state):
    rd, rs1, imm = args
    addr = state['registers'][rs1] + imm
    word = state['memory'][addr:addr+4].view('<u4')[0]
    state['registers'][rd] = word
    
@register_instr('lbu')
def instr_lbu(args, state):
    rd, rs1, imm = args
    addr = state['registers'][rs1] + imm
    state['registers'][rd] = zero_ext(state['memory'][addr])

@register_instr('lhu')
def instr_lhu(args, state):
    rd, rs1, imm = args
    addr = state['registers'][rs1] + imm
    halfword = state['memory'][addr:addr+2].view('<u2')[0]
    state['registers'][rd] = zero_ext(halfword)
    
@register_instr('jalr') # TODO: review
def instr_jalr(args, state):
    rd, rs1, imm = args
    temp = state['pc'] + 4
    state['pc'] = (state['registers'][rs1] + imm) & ~1
    state['registers'][rd] = temp

# S type instructions  TODO: fix sh and sw
@register_instr('sb')
def instr_sb(args, state):
    rs1, rs2, imm = args
    addr = state['registers'][rs1] + imm
    state['memory'][addr] = (state['registers'][rs2] & 0xFF).astype(np.uint8)

@register_instr('sh')
def instr_sh(args, state):
    rs1, rs2, imm = args
    addr = state['registers'][rs1] + imm
    val = state['registers'][rs2] & 0xFFFF
    val_array = np.array([val], dtype='<u2')
    state['memory'][addr:addr+2] = val_array.tobytes()

@register_instr('sw')
def instr_sw(args, state):
    rs1, rs2, imm = args
    addr = state['registers'][rs1] + imm
    val = state['registers'][rs2]
    state['memory'][addr:addr+4] = np.frombuffer(val.to_bytes(4, byteorder='little'), dtype=np.uint8)

# J type instructions

@register_instr('jal')
def instr_jal(args, state):
    rd, imm = args
    state['registers'][rd] = state['pc'] + 4
    state['pc'] += imm - 4

# B type instructions

@register_instr('beq')
def instr_beq(args, state):
    rs1, rs2, imm = args
    if state['registers'][rs1] == state['registers'][rs2]:
        state['pc'] += imm - 4

@register_instr('bne')
def instr_bne(args, state):
    rs1, rs2, imm = args
    if state['registers'][rs1] != state['registers'][rs2]:
        state['pc'] += imm - 4

@register_instr('blt')
def instr_blt(args, state):
    rs1, rs2, imm = args
    if signed(state['registers'][rs1]) < signed(state['registers'][rs2]):
        state['pc'] += imm - 4

@register_instr('bge')
def instr_bge(args, state):
    rs1, rs2, imm = args
    if signed(state['registers'][rs1]) > signed(state['registers'][rs2]):
        state['pc'] += imm - 4

@register_instr('bltu')
def instr_bltu(args, state):
    rs1, rs2, imm = args
    if state['registers'][rs1] < state['registers'][rs2]:
        state['pc'] += imm - 4

@register_instr('bgeu')
def instr_bgeu(args, state):
    rs1, rs2, imm = args
    if state['registers'][rs1] > state['registers'][rs2]:
        state['pc'] += imm - 4
        
# U type instructions

@register_instr('lui')
def instr_lui(args, state):
    rd, imm = args
    state['registers'][rd] = (imm << 12)

@register_instr('auipc')
def instr_auipc(args, state):
    rd, imm = args
    state['registers'][rd] = state['pc'] + (imm << 12)

# utils

def signed(num):
    return num if num < 2**32 else num - 2**33

def sign_ext(value, k):
    """
    Sign extends a k bit number to 32 bits
    """
    value = int(value)
    extended = value if value < (1 << (k - 1)) else value - (1 << k)
    return np.uint32(extended)

def zero_ext(value):
    """
    Zero extends number to 32 bits
    """
    value = int(value)
    return np.uint32(value)
