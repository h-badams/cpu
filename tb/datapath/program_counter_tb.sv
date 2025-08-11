// testbench for pc

`timescale 1ns/10ps

module program_counter_tb ();

    logic [31:0] pc_in;
    logic [31:0] pc_out;
    logic clk, reset;

    program_counter dut (.clk(clk), .reset(reset), .next(pc_in), .pc(pc_out));

    parameter CLOCK_PERIOD = 10;

    initial begin
        clk <= 0;
        forever #(CLOCK_PERIOD/2) clk <= ~clk;
    end

    initial begin
        reset <= 1; pc_in <= 32'h0000_0008; @(posedge clk);
        reset <= 0;                         @(posedge clk);
        pc_in <= 32'h0000_0004;             @(posedge clk);
                                            @(posedge clk);
        pc_in <= 32'h0000_0008;             @(posedge clk);
                                            @(posedge clk);
        pc_in <= 32'h0000_002C;             @(posedge clk);
                                            @(posedge clk);
        reset <= 1;                         @(posedge clk);
        reset <= 0;                         @(posedge clk);
        pc_in <= 32'h0000_0010;             @(posedge clk);
                                            @(posedge clk);

        $stop;
    end

    

endmodule