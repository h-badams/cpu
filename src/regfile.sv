// regfile

module regfile(
    input logic clk,

    input logic we3, // write enable
    input logic [4:0] wa3, // write address
    input logic [31:0] wd3, // write data

    input logic [4:0] ra1, // read address 1
    input logic [4:0] ra2, // read address 2
    output logic [31:0] rd1, // read data 1
    output logic [31:0] rd2 // read data 2
);

    logic [31:0] registers [0:31];

    always_ff @(posedge clk) begin
        // write logic
        if (we3 && wa3 != 5'b0) begin
            registers[wa3] <= wd3;
        end
    end

    always_comb begin
        rd1 = registers[ra1];
        rd2 = registers[ra2];
    end

endmodule
