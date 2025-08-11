// testbench for ALU module
`timescale 1ns/10ps

module alu_tb();

    parameter DELAY_PERIOD = 100;

    logic [31:0] a, b;
    logic [2:0] alu_control;
    logic [31:0] result;
    logic zero;

    integer i;

    alu dut (
        .a(a),
        .b(b),
        .alu_control(alu_control),
        .result(result),
        .zero(zero)
    );

    // Force %t's to print in a nice format.
    initial $timeformat(-9, 2, " ns", 10);

    initial begin
        // Initialize inputs
        a <= 32'h00000000;
        b <= 32'h00000000;
        alu_control <= 3'b000;
        #(DELAY_PERIOD);

        // Test basic arithmetic operations
        $display("%t Testing basic arithmetic operations", $time);
        
        // Test ADD operation (alu_control = 000)
        a <= 32'h12345678;
        b <= 32'h87654321;
        alu_control <= 3'b000;
        #(DELAY_PERIOD);
        $display("%t ADD: %h + %h = %h, zero = %b", $time, a, b, result, zero);

        // Test SUB operation (alu_control = 001)
        a <= 32'h87654321;
        b <= 32'h12345678;
        alu_control <= 3'b001;
        #(DELAY_PERIOD);
        $display("%t SUB: %h - %h = %h, zero = %b", $time, a, b, result, zero);

        // Test AND operation (alu_control = 010)
        a <= 32'hAAAAAAAA;
        b <= 32'h55555555;
        alu_control <= 3'b010;
        #(DELAY_PERIOD);
        $display("%t AND: %h & %h = %h, zero = %b", $time, a, b, result, zero);

        // Test OR operation (alu_control = 011)
        a <= 32'hAAAAAAAA;
        b <= 32'h55555555;
        alu_control <= 3'b011;
        #(DELAY_PERIOD);
        $display("%t OR:  %h | %h = %h, zero = %b", $time, a, b, result, zero);

        // Test SLT operation (alu_control = 101)
        a <= 32'h00000005;
        b <= 32'h0000000A;
        alu_control <= 3'b101;
        #(DELAY_PERIOD);
        $display("%t SLT: %h < %h = %h, zero = %b", $time, a, b, result, zero);

        // Test SLT with negative numbers
        a <= 32'hFFFFFFFE; // -2
        b <= 32'h00000001; // 1
        alu_control <= 3'b101;
        #(DELAY_PERIOD);
        $display("%t SLT: %h < %h = %h, zero = %b", $time, a, b, result, zero);

        // Test comprehensive pattern with all defined operations
        $display("%t Testing all ALU operations with pattern", $time);
        for (i=0; i<8; i=i+1) begin
            a <= 32'h00000010 + i;
            b <= 32'h00000005 + i;
            alu_control <= i[2:0];
            #(DELAY_PERIOD);
            $display("%t Op[%b]: a=%h, b=%h, result=%h, zero=%b", $time, alu_control, a, b, result, zero);
        end

        // Test Zero flag conditions
        $display("%t Testing Zero flag conditions", $time);
        
        // Test subtraction resulting in zero
        a <= 32'h12345678;
        b <= 32'h12345678;
        alu_control <= 3'b001; // SUB
        #(DELAY_PERIOD);
        $display("%t Zero test SUB: %h - %h = %h, zero = %b", $time, a, b, result, zero);

        // Test AND resulting in zero
        a <= 32'hAAAAAAAA;
        b <= 32'h55555555;
        alu_control <= 3'b010; // AND
        #(DELAY_PERIOD);
        $display("%t Zero test AND: %h & %h = %h, zero = %b", $time, a, b, result, zero);

        // Test SLT resulting in zero (when a >= b)
        a <= 32'h0000000A;
        b <= 32'h00000005;
        alu_control <= 3'b101; // SLT
        #(DELAY_PERIOD);
        $display("%t Zero test SLT: %h < %h = %h, zero = %b", $time, a, b, result, zero);

        // Test edge cases
        $display("%t Testing edge cases", $time);
        
        // Test with all zeros
        a <= 32'h00000000;
        b <= 32'h00000000;
        alu_control <= 3'b000; // ADD
        #(DELAY_PERIOD);
        $display("%t Edge case - zeros ADD: %h + %h = %h, zero = %b", $time, a, b, result, zero);

        // Test with all ones
        a <= 32'hFFFFFFFF;
        b <= 32'hFFFFFFFF;
        alu_control <= 3'b010; // AND
        #(DELAY_PERIOD);
        $display("%t Edge case - ones AND: %h & %h = %h, zero = %b", $time, a, b, result, zero);

        // Test undefined operation (should default to 0)
        a <= 32'h12345678;
        b <= 32'h87654321;
        alu_control <= 3'b100; // undefined
        #(DELAY_PERIOD);
        $display("%t Undefined op test: alu_control=%b, result=%h, zero = %b", $time, alu_control, result, zero);

        $stop;
    end
endmodule