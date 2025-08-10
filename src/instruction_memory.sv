// instruction memory

module instruction_memory (
    input logic [31:0] addr,
    output logic [31:0] instr
);

    logic [31:0] mem [0:255];

    assign instr = mem[addr[9:2]]; // word-aligned address

endmodule
