# assembler from risc-v 32I to machine code

import numpy as np

def to_machine_code(filepath):
    raw_instructions = parse_file(filepath)
    instructions = resolve_labels(raw_instructions)
    operands = classify_operands(instructions)
    machine_code = encode_instructions(operands) # gives a numpy array
    return machine_code

def parse_file(filepath):
    '''
    Returns a list of instructions from a txt file.
    instructions are returned as tuples, like
    ('add', 'x0', 'x1', 'x2')
    also contains labels as ('loop:',)
    '''
    
    text = get_file_text(filepath)
    instructions = []
    
    lines = text.split("\n")
        
    for line in lines:
        
        # remove comments
        idx = line.find('#')
        if idx != -1:
            line = line[0:idx]
        
        # separate labels
        idx = line.find(':')
        if idx != -1:
            label = line[0:idx]
            line = line[idx+1:]
            label = label.strip()
            instructions.append((label, 'LABEL'))
        
        line = line.strip()
        if len(line) > 0:
            instructions.append(parse_line(line))

    return instructions

def resolve_labels(instructions):
    '''
    Replaces all instances of labels with their correct address
    '''
    pc = 0
    label_to_addr = {}
        
    for instr in instructions:     
        if len(instr) == 2 and instr[1] == 'LABEL':
            label_to_addr[instr[0]] = pc
        else:
            pc += 4
    
    pc = 0
    resolved = []

    for instr in instructions:
        if len(instr) == 2 and instr[1] == 'LABEL':
            continue
        
        opcode = instr[0]
        label = instr[-1]

        if opcode in {'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu', 'jal'}:
            if is_number(label):
                resolved.append(instr)
            elif label in label_to_addr:
                offset = label_to_addr[label] - pc
                label = str(offset)
                resolved.append((*instr[:-1], label))
            else:
                raise ValueError(f"label \"{label}\" is unknown")
        else:
            resolved.append(instr)  
        pc += 4
        
    return resolved

def classify_operands(instructions):
    '''
    Takes instructions and returns a list of dicts of more easily encoded instructions
    I.e. [('beq', 'x0', 'x1', -8)] -> [{'type': 'B', 'op': 'beq', 'rs1': 0, 'rs2': 1, 'imm': -8}]
    '''
    type_to_instr = {
        'R': {'add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and'},
        'I': {'addi', 'slti', 'sltiu', 'xori', 'ori', 'andi', 'slli', 'srli', 
            'srai', 'jalr', 'lb', 'lh', 'lw', 'lbu', 'lhu'},
        'S': {'sb', 'sh', 'sw'},
        'B': {'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu'},
        'U': {'lui', 'auipc'},
        'J': {'jal'}
    }
    classification = []
    for i, instr in enumerate(instructions):
        operands = instr[1:]
        op = instr[0]
        fmt = None
        for type in {'R', 'I', 'S', 'B', 'U', 'J'}:
            if op in type_to_instr[type]:
                fmt = type
        if fmt is None:
            raise ValueError(f"unknown instruction type: {instr[0]}")
        try:
            if fmt == 'R':
                rd, rs1, rs2 = operands
                rd = reg_name_to_num(rd)
                rs1 = reg_name_to_num(rs1)
                rs2 = reg_name_to_num(rs2)
                classification.append(
                    {'type': fmt, 'op': op, 'rd': rd, 'rs1': rs1, 'rs2': rs2}
                    )
            elif fmt == 'I':
                if '(' in operands[1]:
                    rd = operands[0]
                    imm, rs1 = parse_memory_operand(operands[1])
                else:
                    rd, rs1, imm = operands
                rd = reg_name_to_num(rd)
                rs1 = reg_name_to_num(rs1)
                imm = int(imm, 0)
                classification.append(
                    {'type': fmt, 'op': op, 'rd': rd, 'rs1': rs1, 'imm': imm})
            elif fmt == 'S':
                rs2 = operands[0]
                imm, rs1 = parse_memory_operand(operands[1])
                rs1 = reg_name_to_num(rs1)
                rs2 = reg_name_to_num(rs2)
                imm = int(imm, 0)
                classification.append(
                    {'type': fmt, 'op': op, 'rs1': rs1, 'rs2': rs2, 'imm': imm})
            elif fmt == 'B':
                rs1, rs2, imm = operands
                rs1 = reg_name_to_num(rs1)
                rs2 = reg_name_to_num(rs2)
                imm = int(imm, 0)
                classification.append(
                    {'type': fmt, 'op': op, 'rs1': rs1, 'rs2': rs2, 'imm': imm})
            elif fmt == 'U':
                rd, imm = operands
                rd = reg_name_to_num(rd)
                imm = int(imm, 0)
                classification.append(
                    {'type': fmt, 'op': op, 'rd': rd, 'imm': imm})
            elif fmt == 'J':
                rd, imm = operands
                rd = reg_name_to_num(rd)
                imm = int(imm, 0)
                classification.append(
                    {'type': fmt, 'op': op, 'rd': rd, 'imm': imm})
        except:
            raise ValueError(f"error on instruction {i}: {instr}")
        
    return classification

def encode_instructions(instructions):
    '''
    Takes a list of classified instruction dictionaries
    Returns a list of 32-bit encoded instruction integers
    '''
    encoded = []

    for ins in instructions:
        
        instr = 0
        
        fmt = ins['type']
        op = ins['op']

        if fmt == 'R':
            rd = ins['rd']
            rs1 = ins['rs1']
            rs2 = ins['rs2']
            
            instr |= rs2 << 20
            instr |= rs1 << 15
            instr |= rd << 7

            op_to_func = {'add' : (0x0, 0x0), 'sub' : (0x0, 0x20), # func3, func7
                          'xor': (0x4, 0x0), 'or' : (0x6, 0x0), 'and' : (0x7, 0x0),
                          'sll' : (0x1, 0x0), 'srl' : (0x5, 0x0), 'sra' : (0x5, 0x20),
                          'slt' : (0x2, 0x0), 'sltu' : (0x3, 0x0)}

            if op not in op_to_func:
                raise ValueError(f"Unknown instruction: {op}")

            func3, func7 = op_to_func[op]
            instr |= func3 << 12
            instr |= func7 << 25

            instr |= 0b0110011 # opcode
        elif fmt == 'I':
            rd = ins['rd']
            rs1 = ins['rs1']
            imm = ins['imm']

            # clip imm to 12 bits
            imm = imm & ((1 << 12) - 1) # TODO decide if we want this, or error checking
            
            instr |= imm << 20
            instr |= rs1 << 15
            instr |= rd << 7

            op_to_func3 = {'addi' : 0x0, 'xori' : 0x4, 'ori' : 0x6,
                            'andi' : 0x7, 'slli' : 0x1, 'srli' : 0x5,
                            'srai' : 0x5, 'slti' : 0x2, 'sltiu' : 0x3,
                            'lb' : 0x0, 'lh' : 0x1, 'lw' : 0x2, 'lbu' : 0x4,
                            'lhu' : 0x5, 'jalr' : 0x0}

            if op not in op_to_func3:
                raise ValueError(f"Unknown instruction: {op}")

            func3 = op_to_func3[op] << 12
            instr |= func3

            if op in {'addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai', 'slti', 'sltiu'}:
                opcode = 0b0010011
            elif op in {'lb', 'lh', 'lw', 'lbu', 'lhu'}:
                opcode = 0b0000011
            elif op == 'jalr':
                opcode = 0b1100111

            instr |= opcode

        elif fmt == 'S':
            # TODO: add throwing errors if reg is greater than 31
            # TODO: add clipping of the immediate, registers (or do we want a value error, IDK)
            rs1 = ins['rs1']
            rs2 = ins['rs2']
            imm = ins['imm']
            
            instr |= rs2 << 20
            instr |= rs1 << 15
            
            imm_11_5 = (imm >> 5) & 0b1111111
            imm_4_0 = imm & 0b11111
            
            instr |= imm_11_5 << 25
            instr |= imm_4_0 << 7

            op_to_func3 = {'sb' : 0b000, 'sh' : 0b001, 'sw' : 0b010}

            if op not in op_to_func3:
                raise ValueError(f"Unknown instruction: {op}")

            func3 = op_to_func3[op] << 12
            instr |= func3

            instr |= 0b0100011 # opcode
        elif fmt == 'B':
            rs1 = ins['rs1']
            rs2 = ins['rs2']
            imm = ins['imm']

            instr |= rs2 << 20
            instr |= rs1 << 15
            
            imm_12 = (imm >> 12) & 1
            imm_11 = (imm >> 11) & 1
            imm_10_5 = (imm >> 5) & 0b111111
            imm_4_1 = (imm >> 1) & 0b1111
            
            instr |= imm_12 << 31
            instr |= imm_10_5 << 25
            instr |= imm_4_1 << 8
            instr |= imm_11 << 7

            op_to_func3 = {'beq' : 0b0, 'bne' : 0b1, 'blt' : 0b100,
                           'bge' : 0b101, 'bltu' : 0b110, 'bgeu' : 0b111}
            
            if op not in op_to_func3:
                raise ValueError(f"Unknown instruction: {op}")

            func3 = op_to_func3[op] << 12
            instr |= func3

            instr |= 0b1100011 # opcode
        elif fmt == 'U':
            rd = ins['rd']
            imm = ins['imm']

            instr |= rd << 7
            
            imm_31_12 = (imm >> 12) & ((1 << 20) - 1)
            instr |= imm_31_12 << 12

            op_to_opcode = {'lui' : 0b0110111, 'auipc' : 0b0010111}

            if op not in op_to_opcode:
                raise ValueError(f"Unknown instruction: {op}")

            opcode = op_to_opcode[op]

            instr |= opcode
        elif fmt == 'J':
            rd = ins['rd']
            imm = ins['imm']

            imm_20 = (imm >> 20) & 1
            imm_19_12 = (imm >> 12) & 0b11111111
            imm_11 = (imm >> 11) & 1
            imm_10_1 = (imm >> 1) & 0b1111111111

            instr |= imm_20 << 31
            instr |= imm_10_1 << 21
            instr |= imm_11 << 20
            instr |= imm_19_12 << 12

            instr |= rd << 7
            instr |= 0b1101111 # opcode
        else:
            raise ValueError(f"Unknown format: {fmt}")

        encoded.append(instr)
    
    encoded = np.array(encoded, dtype=np.uint32)

    return encoded


def parse_line(line):
    return tuple(line.replace(",", " ").split())

def get_file_text(filepath):
    with open(filepath) as f:
        x = f.read()
    return x

def is_number(s):
    try:
        int(s, 0)
        return True
    except:
        return False

def reg_name_to_num(reg):
    if reg[0] == 'x':
        return int(reg[1:])
    raise ValueError(f"Invalid register name: {reg}")

def parse_memory_operand(s):
    idx_l = s.find('(')
    idx_r = s.find(')')
    offset = s[:idx_l]
    reg = s[idx_l+1:idx_r]
    return offset, reg