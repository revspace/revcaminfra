#!/bin/bash

while true;
	do date;
	echo Video input $1, source on UDP port 900$1, sink on TCP port 900$1;
	echo;
	gst-launch-1.0 -e udpsrc port=900$1 \
	! application/x-rtp,media=video,payload=121,clock-rate=90000,encoding-name=MP4V-ES,profile-level-id=1  \
	! rtpmp4vdepay  \
	! decodebin  \
	! videoscale \
	! video/x-raw,width=640,height=480 \
	! jpegenc  \
	! multipartmux boundary=RevSpaceCam  \
	! tcpserversink host=localhost port=900$1;
	echo;
	echo;
done 2>&1 | tee -a gst_input$1.log;
