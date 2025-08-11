// datapath
// currently supports 9 instructions, see the design doc

module datapath (
    input logic clk, reset,

    // control signals
    input logic mem_write,
    input logic reg_write,
    input logic [2:0] alu_control,
    input logic [1:0] imm_src,
    input logic [1:0] result_src,

    input logic pc_src,
    input logic alu_src,

    output logic zero,
    output logic [31:0] instr
);

    logic [31:0] pc;
    logic [31:0] pc_next;
    logic [31:0] result;
    logic [31:0] rd1;
    logic [31:0] rd2;

    logic [31:0] imm_ext;
    logic [31:0] alu_b;

    logic [31:0] alu_result;
    logic [31:0] data_rd;
    logic [31:0] pc_plus4;
    logic [31:0] pc_target;

    program_counter program_counter (.clk(clk), .reset(reset), .next(pc_next), .pc(pc));

    assign pc_plus4 = pc + 4;
    assign pc_target = pc + imm_ext;

    instruction_memory instruction_memory (.addr(pc), .instr(instr));

    sign_extender sign_extender (.instr(instr), .control(imm_src), .imm(imm_ext));

    mux2_1 pc_next_mux (.in0(pc_plus4), .in1(pc_target), .select(pc_src), .out(pc_next));

    regfile regfile (.clk(clk), .reset(reset), .we3(reg_write), .ra1(instr[19:15]), .ra2(instr[24:20]),
                    .wa3(instr[11:7]), .wd3(result), .rd1(rd1), .rd2(rd2)
    );

    mux2_1 alu_b_mux (.in0(rd2), .in1(imm_ext), .select(alu_src), .out(alu_b));

    alu alu (.a(rd1), .b(alu_b), .alu_control(alu_control), .result(alu_result), .zero(zero));

    data_memory data_memory (
        .clk(clk),
        .we(mem_write),
        .addr(alu_result),
        .wd(rd2),
        .rd(data_rd)
    );

    mux4_1 result_mux (
        .in0(alu_result),
        .in1(data_rd),
        .in2(pc_plus4),
        .in3(32'b0), // unused
        .select(result_src),
        .out(result)
    );


endmodule
