#!/bin/bash
service apache2 start
dxr-serve.py -h $HOSTNAME /dxr/tests/test_basic/target
