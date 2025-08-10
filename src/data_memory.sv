// data memory

module data_memory (
    input logic clk,

    input logic we, // write enable
    input logic [31:0] addr, // address
    input logic [31:0] wd, // write data

    output logic [31:0] rd // read data
);

    logic [31:0] mem [0:255];

    always_ff @(posedge clk) begin
        if (we) begin
            mem[addr[9:2]] <= wd; // word-aligned address
        end
    end

    assign rd = mem[addr[9:2]];

endmodule
