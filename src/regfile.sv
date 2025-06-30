// regfile

module regfile(
    input logic clk;
    input logic reset;

    input logic write_enable;
    input logic [4:0] write_addr;
    input logic [31:0] write_data;

    input logic [4:0] read_addr1;
    input logic [4:0] read_addr2;
    output logic [31:0] read_data1;
    output logic [31:0] read_data2;
);

    logic [31:0] registers [0:31];

    always_ff @(posedge clk) begin
        // reset logic
        if (reset) begin
            for (int i = 0; i < 32; i++) begin
                registers[i] <= 32'b0;
            end
        end
        // write logic
        if (write_enable && write_addr != 5'b0) begin
            registers[write_addr] <= write_data;
        end

    end

    always_comb begin
        read_data1 = registers[read_addr1];
        read_data2 = registers[read_addr2];
    end

endmodule
