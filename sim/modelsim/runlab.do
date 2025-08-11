# Create work library
vlib work

# Compile Verilog
#     All Verilog files that are part of this design should have
#     their own "vlog" line below.

# SV Files here:
vlog "../../src/alu_decoder.sv"
vlog "../../src/alu.sv"
vlog "../../src/control.sv"
vlog "../../src/cpu.sv"
vlog "../../src/data_memory.sv"
vlog "../../src/datapath.sv"
vlog "../../src/instruction_memory.sv"
vlog "../../src/main_decoder.sv"
vlog "../../src/mux.sv"
vlog "../../src/program_counter.sv"
vlog "../../src/regfile.sv"
vlog "../../src/sign_extender.sv"

# TestBench Files here:

vlog "../../tb/control/alu_decoder_tb.sv"
vlog "../../tb/control/main_decoder_tb.sv"
vlog "../../tb/cpu/cpu_tb.sv"
vlog "../../tb/datapath/alu_tb.sv"
vlog "../../tb/datapath/data_memory_tb.sv"
vlog "../../tb/datapath/instruction_memory_tb.sv"
vlog "../../tb/datapath/mux_tb.sv"
vlog "../../tb/datapath/program_counter_tb.sv"
vlog "../../tb/datapath/regfile_tb.sv"
vlog "../../tb/datapath/sign_extender_tb.sv"


# Call vsim to invoke simulator
#     Make sure the last item on the line is the name of the
#     testbench module you want to execute.
vsim -voptargs="+acc" -t 1ps -lib work alu_tb

# Source the wave do file
#     This should be the file that sets up the signal window for
#     the module you are testing.
do alu_tb.do

# Set the window types
view wave
view structure
view signals

# Run the simulation
run -all