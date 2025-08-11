onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -radix hexadecimal /alu_tb/a
add wave -noupdate -radix hexadecimal /alu_tb/b
add wave -noupdate /alu_tb/alu_control
add wave -noupdate -radix hexadecimal /alu_tb/result
add wave -noupdate /alu_tb/zero
add wave -noupdate /alu_tb/i
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {40134 ps} 0}
quietly wave cursor active 1
configure wave -namecolwidth 150
configure wave -valuecolwidth 128
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
WaveRestoreZoom {0 ps} {147629 ps}
