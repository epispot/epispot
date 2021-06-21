#!/bin/bash
# checks epispot nightly release codes and returns a pass/fail exit status
if [[ $1 = $2 ]]
then
    echo "Exited with 0; security codes match"
    exit 0
else
    echo "Exited with 1; security codes don't match"
    exit 1
fi
