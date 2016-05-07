; --- Test HIGHWORD operator
; --- In version 2.12pre the operator was broken.


	.386
	.model flat
	
	.data
	
	x = 0FEDCBA98h
	
	; case: MSB set
	dd HIGHWORD x
	
	; upper 32 bits are not zeroed by HIGHWORD
	dd HIGH32 (HIGHWORD (x SHL 32))
	
	; for compare the upper 32 bits
	dd HIGH32 (x SHL 32)
	
	
	; repeat test for case: MSB cleared
	y = 07EDCBA98h
	dd HIGHWORD y
	dd HIGH32 (HIGHWORD (y SHL 32))
	dd HIGH32 (y SHL 32)
	
	END

	