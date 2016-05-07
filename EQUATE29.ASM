; --- Test reuse of assembly time variables as label for INSTR and SIZESTR.
; --- In version 2.12pre there is a bug in function CreateVariable, equate.c
; --- where the upper 32 bits of reused equates is not set to zero.


	.386
	.model flat
	
	.data
	
	x = -1              ; bits 0...63 are set
	
	x INSTR <abc>,<b>   ; x should be 2
	
	; by definition of INSTR this compare should always evaluate to true (-1 for MASM)
	IF x GE 0
		db 1
	ELSE
		db 0
	ENDIF 
	
	x = -1
	
	; the same for SIZESTR
	x SIZESTR <1234>
	IF x GE 0
		db 1
	ELSE
		db 0
	ENDIF 
	
	; should be zero
	dd HIGH32 x
	
	
	END