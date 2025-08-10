// alu decoder
// currently supports the 9 instructions in the design doc

module alu_decoder (
    input logic [2:0] funct3,
    input logic funct7_5,
    input logic opcode_5,

    input logic [1:0] alu_op,

    output logic [2:0] alu_control
);

    always_comb begin
        case (alu_op)
            2'b00: alu_control = 3'b000; // lw, sw
            2'b01: alu_control = 3'b001; // beq
            2'b10: begin // R-type
                case (funct3)
                    3'b000: begin
                        case ({opcode_5, funct7_5})
                            2'b00: alu_control = 3'b000;
                            2'b01: alu_control = 3'b000;
                            2'b10: alu_control = 3'b000;
                            2'b11: alu_control = 3'b001;
                        endcase
                    end
                    3'b010: alu_control = 3'b101;
                    3'b110: alu_control = 3'b101;
                    3'b111: alu_control = 3'b010;
                    default: alu_control = 3'b111; // invalid
                endcase
            end
            default: alu_control = 3'b111; // invalid
        endcase
    end


endmodule
