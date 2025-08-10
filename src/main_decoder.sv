// main decoder for the control unit
// currently supports the 9 instructions in the design doc

module main_decoder (
    input logic [6:0] opcode,

    output logic mem_write,
    output logic reg_write,
    output logic [1:0] alu_op,
    output logic [1:0] imm_src,
    output logic [1:0] result_src,

    output logic branch,
    output logic jump,
    output logic alu_src
);

    always_comb begin // reg_write 
        case (opcode)
            7'b0000011: reg_write = 1'b1; // lw
            7'b0110011: reg_write = 1'b1; // R-type
            7'b1101111: reg_write = 1'b1; // jal
            default: reg_write = 1'b0;
        endcase
    end

    always_comb begin // imm_src
        case (opcode)
            7'b0000011: imm_src = 2'b00; // lw
            7'b0100011: imm_src = 2'b01; // sw
            7'b1100011: imm_src = 2'b10; // beq
            7'b1101111: imm_src = 2'b11; // jal
            default: imm_src = 2'b00;
        endcase
    end

    always_comb begin // alu_src
        case (opcode)
            7'b0000011: alu_src = 1'b1; // lw
            7'b0100011: alu_src = 1'b1; // sw
            7'b0110011: alu_src = 1'b0; // R-type
            7'b1100011: alu_src = 1'b0; // beq
            default: alu_src = 1'b0;
        endcase
    end

    always_comb begin // mem_write
        case (opcode)
            7'b0100011: mem_write = 1'b1; // sw
            default: mem_write = 1'b0;
        endcase
    end

    always_comb begin // result_src
        case (opcode)
            7'b0000011: result_src = 2'b01; // lw
            7'b0110011: result_src = 2'b00; // R-type
            7'b1101111: result_src = 2'b10; // jal
            default: result_src = 2'b00;
        endcase
    end

    always_comb begin // branch
        case (opcode)
            7'b1100011: branch = 1'b1; // beq
            default: branch = 1'b0;
        endcase
    end

    always_comb begin // alu_op
        case (opcode)
            7'b0000011: alu_op = 2'b00; // lw
            7'b0100011: alu_op = 2'b00; // sw
            7'b0110011: alu_op = 2'b10; // R-type
            7'b1100011: alu_op = 2'b01; // beq
            default: alu_op = 2'b00;
        endcase
    end

    always_comb begin // jump
        case (opcode)
            7'b1101111: jump = 1'b1; // jal
            default: jump = 1'b0;
        endcase
    end

endmodule
