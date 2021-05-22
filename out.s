.text
main:
	li $s1, 1
	li $s0, 5
	li $s2, 1
L0:
	la $t0, false
	bge $s1, $s0, SKIP0
	la $t0, true
SKIP0:
	la $t1, true
	beq $t1, $t0, kogda0
L1:
	li $t0, 2
	li $t1, 5
	div $t0, $t1
	move $s3, $t0
	li $v0, 1
	la $a0, ($s3)
	syscall
	j END
kogda0:
	li $s6, 1
	move $a0, $s1
	move $a1, $s2
	move $a2, $s6
	jal fact
	move $t1, $t9
	move $s6, $t1
	li $v0, 1
	la $a0, ($s6)
	syscall
	li $v0, 4
	la $a0, str0
	syscall
	li $t1, 1
	addu $t0, $s1, $t1
	move $s1, $t0
	j L0
fact:
L2:
	la $t0, false
	bge $a1, $a0, SKIP1
	la $t0, true
SKIP1:
	la $t1, true
	beq $t1, $t0, kogda1
L3:
	mult $a2, $a0
	mflo $t0
	move $t9, $t0
	jr $ra
kogda1:
	mult $a2, $a1
	mflo $t1
	move $a2, $t1
	li $t1, 1
	addu $t0, $a1, $t1
	move $a1, $t0
	j L2
END:
.data
	true: .byte 1
	false: .byte 0
	str0: .asciiz ","
