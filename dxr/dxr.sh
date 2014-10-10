#!/bin/bash
service apache2 start
dxr-serve.py -h $HOSTNAME /storage/local/data1/gartung/dxr/tests/test_basic/target
