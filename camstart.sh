#!/bin/bash

screen -S cam7_input7 -X kill
screen -S cam8_input8 -X kill
screen -S cam9_input6 -X kill
screen -S cam_server_py -X kill

screen -dmS cam7_input7 bash -c './gst.sh 7'
screen -dmS cam8_input8 bash -c './gst.sh 8'
screen -dmS cam9_input6 bash -c './gst.sh 6'
screen -dmS cam_server_py bash -c './server.py 2>&1 > server_py.log'
