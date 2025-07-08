// program counter
// increments to next every clock cycle

module program_counter (
    input logic clk, reset,
    input logic [31:0] next,
    output logic [31:0] pc
);

    always_ff @(posedge clk) begin
        if (reset) begin
            pc <= 32'b0;
        end else begin
            pc <= next;
        end
    end

endmodule
