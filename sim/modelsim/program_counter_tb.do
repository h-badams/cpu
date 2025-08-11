onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /program_counter_tb/pc_in
add wave -noupdate /program_counter_tb/pc_out
add wave -noupdate /program_counter_tb/clk
add wave -noupdate /program_counter_tb/reset
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {18392 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 179
configure wave -valuecolwidth 206
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 50
configure wave -gridperiod 100
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ps} {27667 ps}
