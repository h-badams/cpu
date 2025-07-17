from assembler import parse_file, resolve_labels, classify_operands, encode_instructions

x = parse_file("emulator/program.txt")
print(x)
print("\n")
y = resolve_labels(x)
print(y)
print("\n")
z = classify_operands(y)
print(z)
print("\n")
a = encode_instructions(z)
print([bin(i)[2:].zfill(32) for i in a])
print(*["\n"+hex(i)[2:].zfill(8) for i in a])

