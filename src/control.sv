// control unit

module control (
    input logic [31:0] instr,
    input logic zero,

    output logic mem_write,
    output logic reg_write,
    output logic [2:0] alu_control,
    output logic [1:0] imm_src,
    output logic [1:0] result_src,

    output logic pc_src,
    output logic alu_src
);

    logic branch;
    logic jump;
    logic [1:0] alu_op;

    main_decoder main_decoder (
        .opcode(instr[6:0]),
        .mem_write(mem_write),
        .reg_write(reg_write),
        .imm_src(imm_src),
        .result_src(result_src),
        .alu_op(alu_op),
        .branch(branch),
        .jump(jump),
        .alu_src(alu_src)
    );

    alu_decoder alu_decoder (
        .funct3(instr[14:12]),
        .funct7_5(instr[30]),
        .opcode_5(instr[6]),
        .alu_op(alu_op),
        .alu_control(alu_control)
    );

    assign pc_src = jump | (branch & zero);

endmodule
