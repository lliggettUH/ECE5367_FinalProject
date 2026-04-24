addi $t0, $zero, 5
addi $t1, $zero, 10
add  $t2, $t0, $t1
lw   $t3, 0($t2)
add  $t4, $t3, $t1
addi $t0, $zero, 1
addi $t4, $zero, 4
sub $t4, $t4, $t4
beq $t4, $zero, skip
addi $t4, $t4, 1
lw   $t5, 4($t3)
add  $t6, $t5, $t0 
skip:
addi $t7, $t6, 1      
add  $s0, $t7, $t1
beq  $s0, $t1, 8
add  $s1, $s0, $t0 