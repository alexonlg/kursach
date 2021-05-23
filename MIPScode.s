.text
main:
	li $s0, 11
	li $s1, 0
	li $s2, 1
L0:
	la $t0, false
	ble $s0, $s1, SKIP0
	la $t0, true
SKIP0:
	la $t1, true
	beq $t1, $t0, kogda0
L1:
	j END
kogda0:
	li $t1, 1
	addu $t1, $s1, $t1
	move $s1, $t1
	move $s2, $s1
	move $a0, $s2
	jal kub
	move $t0, $t9
	move $s2, $t0
	li $v0, 1
	la $a0, ($s2)
	syscall
	li $v0, 4
	la $a0, str0
	syscall
	j L0
kub:
	mult $a0, $a0
	mflo $t0
	move $a0, $t0
	mult $a0, $a0
	mflo $t0
	move $t9, $t0
	jr $ra
END:
.data
	true: .byte 1
	false: .byte 0
	str0: .asciiz ","
