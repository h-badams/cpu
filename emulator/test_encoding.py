import numpy as np

from assembler import parse_file, resolve_labels, classify_operands, encode_instructions
from decoder import parse_instruction

x = parse_file("emulator/program.txt")
print(x)
print()
y = resolve_labels(x)
print(y)
print()
z = classify_operands(y)
print(z)
print()
a = encode_instructions(z)
print([bin(i)[2:].zfill(32) for i in a])
print(*["\n"+hex(i)[2:].zfill(8) for i in a])
print()

# convert to bytes (little-endian)
a_le = a.view(dtype=np.uint8).reshape(-1, 4)
print(a_le)

new_instructions = [parse_instruction(i) for i in a_le]
print(new_instructions)

