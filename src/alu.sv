// alu

module alu (
    input logic [31:0] a,
    input logic [31:0] b,
    input logic [2:0] alu_control,
    output logic [31:0] result,
    output logic zero
);

    always_comb begin
        case (alu_control)
            3'b000: result = a + b; 
            3'b001: result = a - b;
            3'b010: result = a & b; 
            3'b011: result = a | b;
            3'b101: begin
                if (signed'(a) < signed'(b)) result = 32'b1;
                else result = 32'b0;
            end
            default: result = 32'b0;
        endcase
    end

    always_comb begin
        if (result == 32'b0) zero = 1'b1;
        else zero = 1'b0;
    end

endmodule


