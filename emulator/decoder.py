import numpy as np

def parse_instruction(instr_arr):
    '''
    Takes a 32-bit instruction and returns the 
    instruction name and its arguments
    '''
    
    instr = (
        instr_arr[3].astype(np.uint32) << 24 |
        instr_arr[2].astype(np.uint32) << 16 |
        instr_arr[1].astype(np.uint32) << 8  |
        instr_arr[0].astype(np.uint32)
    )
    
    # print(bin(instr)[2:].zfill(32))
    
    opcode = instr & 0b1111111
    
    if opcode == 0b0110011:
        return parse_r_type(instr)    
    elif opcode in [0b0010011, 0b0000011, 0b1100111]: # ecall not yet implemented
        return parse_i_type(instr)
    elif opcode == 0b0100011:
        return parse_s_type(instr)
    elif opcode == 0b1100011:
        return parse_b_type(instr)
    elif opcode == 0b1101111:
        return parse_j_type(instr)
    elif opcode in [0b0110111, 0b0010111]:
        return parse_u_type(instr)
    else:
        raise ValueError(f"Unknown opcode: {opcode}")
    
def parse_r_type(instr):
    
    func7 = (instr >> 25) & 0b1111111
    func3 = (instr >> 12) & 0b111
    rs1 = (instr >> 15) & 0b11111
    rs2 = (instr >> 20) & 0b11111
    rd = (instr >> 7) & 0b11111
    
    if func7 == 0x00:
        if func3 == 0x0:
            op = 'add'
        elif func3 == 0x4:
            op = 'xor'
        elif func3 == 0x6:
            op = 'or'
        elif func3 == 0x7:
            op = 'and'
        elif func3 == 0x1:
            op = 'sll'
        elif func3 == 0x5:
            op = 'srl'
        elif func3 == 0x2:
            op = 'slt'
        elif func3 == 0x3:
            op = 'sltu'
        else:
            raise ValueError(f"Unknown R-type func7, func3: {bin(func7)}, {bin(func3)}")
    elif func7 == 0x20:
        if func3 == 0x0:
            op = 'sub'
        elif func3 == 0x5:
            op = 'sra'
        else:
            raise ValueError(f"Unknown R-type func7, func3: {bin(func7)}, {bin(func3)}")
    else:
        raise ValueError(f"Unknown R-type func7, func3: {bin(func7)}, {bin(func3)}")

    return (op, (rd, rs1, rs2))

def parse_i_type(instr):
        
    func3 = (instr >> 12) & 0b111
    rd = (instr >> 7) & 0b11111
    rs1 = (instr >> 15) & 0b11111
    imm = (instr >> 20) & ((1 << 12) - 1)
    imm = sign_ext(imm, 12)

    opcode = instr & 0b1111111
    
    # first check by opcode
    if opcode == 0b0010011:
        if func3 == 0x0:
            op = 'addi'
        elif func3 == 0x2:
            op = 'slti'
        elif func3 == 0x3:
            op = 'sltiu'
        elif func3 == 0x4:
            op = 'xori'
        elif func3 == 0x6:
            op = 'ori'
        elif func3 == 0x7:
            op = 'andi'
        elif func3 == 0x1:
            op = 'slli'
        elif func3 == 0x5:
            if (instr >> 25) & 0b1111111 == 0x00:
                op = 'srli'
            elif (instr >> 25) & 0b1111111 == 0x20:
                op = 'srai'
            else:
                raise ValueError(f"Unknown I-type instruction: {bin(instr)}")
        else:
            raise ValueError(f"Unknown I-type opcode, func3: {bin(opcode)}, {bin(func3)}")
    elif opcode == 0b0000011:
        if func3 == 0x0:
            op = 'lb'
        elif func3 == 0x1:
            op = 'lh'
        elif func3 == 0x2:
            op = 'lw'
        elif func3 == 0x4:
            op = 'lbu'
        elif func3 == 0x5:
            op = 'lhu'
        else:
            raise ValueError(f"Unknown I-type opcode, func3: {bin(opcode)}, {bin(func3)}")
    elif opcode == 0b1100111:
        if func3 == 0x0:
            op = 'jalr'
        else:
            raise ValueError(f"Unknown I-type opcode, func3: {bin(opcode)}, {bin(func3)}")
    else:
        raise ValueError(f"Unknown I-type opcode: {bin(opcode)}")
    
    return (op, (rd, rs1, imm))
    
def parse_s_type(instr):
    
    func3 = (instr >> 12) & 0b111
    rs1 = (instr >> 15) & 0b11111
    rs2 = (instr >> 20) & 0b11111
    
    imm_11_5 = (instr >> 25) & 0b111111
    imm_4_0 = (instr >> 7) & 0b11111
    imm = (imm_11_5 << 5) | imm_4_0
    
    imm = sign_ext(imm, 12)
    
    if func3 == 0x0:
        op = 'sb'
    elif func3 == 0x1:
        op = 'sh'
    elif func3 == 0x2:
        op = 'sw'
    else:
        raise ValueError(f"Unknown S-type func3: {bin(func3)}")
    
    return (op, (rs1, rs2, imm))

def parse_b_type(instr):
    
    func3 = (instr >> 12) & 0b111
    rs1 = (instr >> 15) & 0b11111
    rs2 = (instr >> 20) & 0b11111
    
    imm_12 = (instr >> 31) & 0b1
    imm_11 = (instr >> 7) & 0b1
    imm_10_5 = (instr >> 25) & 0b111111
    imm_4_1 = (instr >> 8) & 0b1111
    
    imm = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
    imm = sign_ext(imm, 13)
    
    if func3 == 0x0:
        op = 'beq'
    elif func3 == 0x1:
        op = 'bne'
    elif func3 == 0x4:
        op = 'blt'
    elif func3 == 0x5:
        op = 'bge'
    elif func3 == 0x6:
        op = 'bltu'
    elif func3 == 0x7:
        op = 'bgeu'
    else:
        raise ValueError(f"Unknown B-type func3: {bin(func3)}")
    
    return (op, (rs1, rs2, imm))

def parse_j_type(instr):
    
    rd = (instr >> 7) & 0b11111
    
    imm_20 = (instr >> 31) & 0b1
    imm_19_12 = (instr >> 12) & 0b11111111
    imm_11 = (instr >> 20) & 0b1
    imm_10_1 = (instr >> 21) & ((1 << 10) - 1)
    
    imm = (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)
    imm = sign_ext(imm, 21)
    
    return ('jal', (rd, imm))
    
def parse_u_type(instr):
    
    rd = (instr >> 7) & 0b11111
    opcode = instr & 0b1111111
    
    imm_31_12 = (instr >> 12) & ((1 << 20) - 1)
    imm = imm_31_12 << 12

    if opcode == 0b0110111:
        op = 'lui'
    elif opcode == 0b0010111:
        op = 'auipc'
    else:
        raise ValueError(f"Unknown U-type opcode: {bin(opcode)}")
    
    return (op, (rd, imm))


def sign_ext(value, k):
    '''
    Sign a k bit number extends to 32 bits
    '''
    return value if value < (1 << (k - 1)) else value - (1 << k)
