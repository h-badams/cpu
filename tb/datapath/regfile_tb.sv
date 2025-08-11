// testbench for register file
`timescale 1ns/10ps

module regfile_tb(); 		

	parameter CLOCK_PERIOD = 100;

	logic [4:0] ReadRegister1, ReadRegister2, WriteRegister;
	logic [31:0] WriteData;
	logic RegWrite, clk, reset;
	logic [31:0] ReadData1, ReadData2;

	integer i;

	regfile dut (
        .clk(clk),
        .reset(reset),
        .we3(RegWrite),
        .wa3(WriteRegister),
        .wd3(WriteData),
        .ra1(ReadRegister1),
        .ra2(ReadRegister2),
        .rd1(ReadData1),
        .rd2(ReadData2)
    );

	// Force %t's to print in a nice format.
	initial $timeformat(-9, 2, " ns", 10);

	initial begin
		clk <= 0;
		forever #(CLOCK_PERIOD/2) clk <= ~clk;
	end

	initial begin
		// Try to write the value 0xA0 into register 0.
        reset <= 1'b1;
        @(posedge clk);
        reset <= 1'b0;
        @(posedge clk);

		RegWrite <= 5'd0;
		ReadRegister1 <= 5'd0;
		ReadRegister2 <= 5'd0;
		WriteRegister <= 5'd0;
		WriteData <= 32'h000000A0;
		@(posedge clk);
		
		$display("%t Attempting overwrite of register 0, which should always be 0", $time);
		RegWrite <= 1'b1;
		@(posedge clk);

		// Write a value into each  register.
		$display("%t Writing pattern to all registers.", $time);
		for (i=0; i<32; i=i+1) begin
			RegWrite <= 0;
			ReadRegister1 <= i-1;
			ReadRegister2 <= i;
			WriteRegister <= i;
			WriteData <= i*32'h00040101;
			@(posedge clk);
			
			RegWrite <= 1;
			@(posedge clk);
		end

		// Go back and verify that the registers
		// retained the data.
		$display("%t Checking pattern.", $time);
		for (i=0; i<32; i=i+1) begin
			RegWrite <= 0;
			ReadRegister1 <= i-1;
			ReadRegister2 <= i;
			WriteRegister <= i;
			WriteData <= i*32'h00040101;
			@(posedge clk);
		end
		$stop;
	end
endmodule