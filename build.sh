#!/bin/bash

echo "Building Victim Image"
docker build -t arplab-victim victim

echo "Building Attacker Image"
docker build -t arplab-attacker attacker
