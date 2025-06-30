// alu

module alu (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [2:0] alu_control,
    output logic [31:0] result,
);

    always_comb begin
        case (alu_control)
            3'b000: result = a & b;
            3'b001: result = a | b;
            3'b010: result = a + b;
            3'b100: result = a & ~b;
            3'b101: result = a | ~b;
            3'b110: result = a - b;
            3'b111: begin
                if (a < b) result = 32'b1;
                else result = 32'b0;
            end
            default: result = 32'b0;
        endcase
    end

endmodule


