#!/bin/bash
envname='crossbar' 

conda create -n $envname python=3.7

eval "$(conda shell.bash hook)"
conda activate $envname;

pip install autobahn twisted
pip install autobahn[serialization]