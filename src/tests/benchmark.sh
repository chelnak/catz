#!/bin/bash

for file in files/*; do
    hyperfine --warmup 3 "catz '$file'" --command-name "catz '$file'"
done