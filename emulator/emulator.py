# for reference:
# https://www.cs.sfu.ca/~ashriram/Courses/CS295/assets/notebooks/RISCV/RISCV_CARD.pdf
# https://msyksphinz-self.github.io/riscv-isadoc/

import numpy as np

from assembler import to_machine_code
from decoder import parse_instruction
from emulator_utils import print_state
from instructions import instruction_table

state = {
    'memory': np.zeros(2**20, dtype=np.uint8),
    'registers': np.zeros(32, dtype=np.uint32),
    'pc': np.uint32(0),
}

file_path = "emulator/program.txt"

instructions = to_machine_code(file_path)
instructions_le = instructions.view(dtype=np.uint8) # convert to little-endian
print(instructions_le)

state['memory'][0:4*instructions.shape[0]] = instructions_le

# main program loop

while state['pc'] < state['memory'].shape[0] - 4:

    instr_bytes = state['memory'][state['pc']:state['pc'] + 4]
    
    if np.all(instr_bytes == 0):
        break

    instr, args = parse_instruction(instr_bytes)
    instruction_table[instr](args, state)
    state['pc'] += 4
    
    # restore invariants
    state['registers'][0] = 0
    
    print_state(state)

print("program finished!")

print_state(state)