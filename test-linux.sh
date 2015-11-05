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

echo ">>"
echo ">> Testing JWasm BIN output"
echo ">>"

jwas

for file in `ls *.[aA][sS][mM]`; do

	blacklisted=`echo $blacklist | grep -w $file`
	if [ ! -z "$blacklisted" ]; then
		printf " - [${YY}BR${NC}] broken $file\n"
		nr_broken=$((nr_broken+1))
		continue;
	fi

	jwasm -q -bin $file &>/dev/null

	`cmp ${file%%.*}.BIN ${file%%.*}.EXP`

	if [ $? -ne 0 ]; then
		printf " - [${RR}ER${NC}] failed $file\n"
		nr_failed=$((nr_failed+1))
	else
		printf " - [${GG}OK${NC}] passed $file\n"
		nr_passed=$((nr_passed+1))
	fi
done

echo ">>"
echo ">> Testing JWasm EXE output"
echo ">>"

blacklist=""

for file in `ls *.[aA][sS][nN]`; do

	blacklisted=`echo $blacklist | grep -w $file`
	if [ ! -z "$blacklisted" ]; then
		printf " - [${YY}BR${NC}] broken $file\n"
		nr_broken=$((nr_broken+1))
		continue;
	fi

	jwasm -q -mz $file &>/dev/null

	`cmp ${file%%.*}.EXE ${file%%.*}.EXP`

	if [ $? -ne 0 ]; then
		printf " - [${RR}ER${NC}] failed $file\n"
		nr_failed=$((nr_failed+1))
	else
		printf " - [${GG}OK${NC}] passed $file\n"
		nr_passed=$((nr_passed+1))
	fi

done

echo "=="
printf "SUMMARY: FAILED ${RR}${nr_failed}${NC} / PASSED ${GG}${nr_passed}${NC} / BROKEN ${YY}${nr_broken}${NC}\n"
echo "=="

exit $nr_failed
