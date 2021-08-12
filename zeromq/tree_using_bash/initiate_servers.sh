#!/bin/bash

# starting at port 1000, create 10 instances
offset=1000
END=10
for index in $(seq 0 $((END-1))); do
    echo $index;
    python3 controller_with_port_as_arg.py $((index+offset)) &
done

