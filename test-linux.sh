#!/bin/sh

RR="\033[0;31m"
GG="\033[0;32m"
YY="\033[1;33m"
NC="\033[0m"

nr_passed=0
nr_failed=0
nr_broken=0

# TODO: resolve all the problems

blacklist="EQUATE4.ASM INVOK648.ASM MOV64.ASM OPATTR2.ASM PROC642.ASM RECORD3.ASM sse2_2.asm"

echo "Testing JWasm BIN output"

for file in `ls *.{ASM,asm}`; do

	if [[ $blacklist =~ $file ]]; then
		echo -e " - [${YY}BR${NC}] broken $file"
		nr_broken=$((nr_broken+1))
		continue;
	fi

	jwasm -bin $file &>/dev/null

	`cmp ${file%%.*}.BIN ${file%%.*}.EXP`

	if [ $? -ne 0 ]; then
		echo -e " - [${RR}ER${NC}] failed $file"
		nr_failed=$((nr_failed+1))
	else
		echo -e " - [${GG}OK${NC}] passed $file"
		nr_passed=$((nr_passed+1))
	fi
done

echo "=="
echo -e "SUMMARY: FAILED ${RR}${nr_failed}${NC} / PASSED ${GG}${nr_passed}${NC} / BROKEN ${YY}${nr_broken}${NC}"
echo "=="

exit $failed