// cpu

module cpu (
    input logic clk,
    input logic reset
);

    logic zero;
    logic [31:0] instr;

    logic mem_write;
    logic reg_write;
    logic [2:0] alu_control;
    logic [1:0] imm_src;
    logic [1:0] result_src;
    logic pc_src;
    logic alu_src;

    datapath datapath (
        .clk(clk),
        .reset(reset),

        .mem_write(mem_write),
        .reg_write(reg_write),
        .alu_control(alu_control),
        .imm_src(imm_src),
        .result_src(result_src),

        .pc_src(pc_src),
        .alu_src(alu_src),

        .zero(zero),
        .instr(instr)
    );

    control control (
        .instr(instr),
        .zero(zero),

        .mem_write(mem_write),
        .reg_write(reg_write),
        .alu_control(alu_control),
        .imm_src(imm_src),
        .result_src(result_src),

        .pc_src(pc_src),
        .alu_src(alu_src)
    );


endmodule