// sign extender

module sign_extender (
    input logic [31:0] instr,
    input logic [1:0] control,
    output logic [31:0] imm

);

    always_comb begin
        case (control)
            2'b00: imm = {{20{instr[31]}}, instr[31:20]}; // I-type
            2'b01: imm = {{20{instr[31]}}, instr[31:25], instr[11:7]}; // S-type
            2'b10: imm = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1'b0}; // B-type
            2'b11: imm = {12{instr[31]}, instr[19:12], instr[20], instr[30:21], 1'b0}; // J-type
            default: imm = 32'b0;
        endcase
    end

endmodule
