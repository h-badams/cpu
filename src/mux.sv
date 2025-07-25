// Multiplexers of various sizes

`timescale 1ns/10ps

// 2:1 mux

module mux2_1 (in, select, out);

    input logic [1:0] in;
    input logic select;
    output logic out;

    always_comb begin
        if (select) out = in[1];
        else out = in[0];
    end

endmodule

// 4:1 mux

module mux4_1 (in, select, out);

    input logic [3:0] in;
    input logic [1:0] select;
    output logic out;

    logic out0, out1;

    mux2_1 mux0 (.in({in[1], in[0]}), .select(select[0]), .out(out0)); // TODO check if the order is wrong in modelsim
    mux2_1 mux1 (.in({in[3], in[2]}), .select(select[0]), .out(out1));
    mux2_1 mux2 (.in({out0, out1}), .select(select[1]), .out(out));

endmodule

// 8:1 mux

module mux8_1 (in, select, out);

    input logic [7:0] in;
    input logic [2:0] select;
    output logic out;

    logic out0, out1;

    mux4_1 mux0 (.in({in[0], in[1], in[2], in[3]}), .select(select[1:0]), .out(out0)); // TODO check if the order is wrong in modelsim
    mux4_1 mux1 (.in({in[4], in[5], in[6], in[7]}), .select(select[1:0]), .out(out1));
    mux2_1 mux2 (.in({out0, out1}), .select(select[2]), .out(out));

endmodule

// TODO add testbench comment

module mux2_1_tb();

    logic [1:0] in;
    logic select, out;

    mux2_1 dut (.in(in), .select(select), .out(out));

    integer i;
    initial begin
        for (i = 0; i < 2**3; i++) begin
            {in, select} = i; #10;
        end
    end

endmodule

// TODO add testbench comment

module mux4_1_tb();

    logic [3:0] in;
    logic [1:0] select;
    logic out;

    mux4_1 dut (.in(in), .select(select), .out(out));

    integer i;
    initial begin
        for (i = 0; i < 2**6; i++) begin
            {in, select} = i; #10;
        end
    end

endmodule

// TODO add testbench

module mux8_1_tb();

    logic [7:0] in;
    logic [2:0] select;
    logic out;

    mux8_1 dut (.in(in), .select(select), .out(out));

    // TODO make a better, shorter testbench

endmodule