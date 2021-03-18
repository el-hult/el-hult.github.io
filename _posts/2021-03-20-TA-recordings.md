---
layout: post
title:  "Recording videos as a TA"
tags: [education, videos, mkv, OBS, Windows Connect, OneNote, mkvmerge, HandBrake]
---

As a PhD student, I am often a teaching assistant (TA) in the courses tought at my department.
With the covid-19-pandemic as a driver, we have more and more started to record lectures and tutorials.
Since I want to learn how to make youtube-quality recordings (that is - not to good and not too bad) I started to read up and try out some tools for theses recordings. The following is a description of a setup that seems to work out okay for my tutorial sessions.
It is definitely not ideal, in many ways, but it is good enough!

# Digital whiteboard - OneNote + Windows Connect
In a tutorial session, I would normally have a whiteboard to work on. 
As a substitute I use the OneNote app on my Samsung Galaxy Tab 6e.
It works well with the S-Pen and gives a really nice write feeling.
I can export the final result as a single long pdf, and that is also good for sharing with the students.
However, I need to get that screen to my recording software!
I choose to fix that using the Connect app in windows 10, which makes the windows computer act as a Miracast screen.
I can then cast my tablet screen to the computer using the Samsung Smart View, which comes bundeled with the standard OS on the tablet.

This setup works with any app on the tablet, since it is a simple screen share. 
I assume it would work with any device that supports Miracast screens as well.

# Recording - OBS
The recording is then done in OBS.
The official homepage is [https://obsproject.com/](https://obsproject.com/). 
There, I can create scenes such as "Snack" ("Chat"), which means recording my face through the laptop webcam, or "Lösning" ("Solution") which features the Micsrosoft Connect app window.
By presing the "Start recording" and "Stop recording" button, it creates .mkv files for each section of the tutorial.

As a side note, the OBS can also export the video stream as a virtual video source e.g. for zoom meetings, so you can have these scene presets in Zoom lectures.

The program has a quite self explenatory GUI interface.

# Merging - mkvmerge
I make sure that each solution is good enough, so that I don't need to do any real editing or cutting work. I just need to stich together a bunch of .mkv-files.

To accomplish that I use [`mkvmerge`](https://mkvtoolnix.download/doc/mkvmerge.html), which is part of MKVToolNix. After installing this software, the following command stiches all sections together. See the documentation for more options.

~~~powershell
PS> & "C:\Program Files\MKVToolNix\mkvmerge.exe" -o tutorial.mkv '[' .\part1.mkv .\part2.mkv .\part3.mkv ']'
~~~

This creates a single .mkv video file. The operation is close to instant since mkv is a container format and it simply pastes the video streams together. There is no video processing of relevance here.

# Compression - HandBrake
If I upload the video to Youtube, it will handle compression for me. N.B. the youtube account needs to be a verified account for videos longer than 15 minutes. See [https://www.youtube.com/verify](https://www.youtube.com/verify).

But when uploading to Studium, the learning platform at Uppsala Universitet based on Canvas by Instructure, there is a 500MB file size limit. So I might have to do some compression!

One simple tool for that is HandBrake, a free open source software available on [https://handbrake.fr/](https://handbrake.fr/). It is a transcoder, so it is super simple and usable for these situations where I don't want to do any editing, but just transcode my file to stronger compression. There is a CLI available, but I used the GUI.

Lets say the duration of the video is 1.5 hours. It has to have total size of 500MB. That means (with rounding...) 

$$
\frac{500 \text{ MB}}{1.5\text{ h}} =
\frac{500 \cdot 8 \text{ Mb}}{1.5 \cdot 3600 \text{ s}} = 
\frac{500 \cdot 8 \cdot 1000\text{ kb}}{1.5 \cdot 3600 \text{ s}} = 
\frac{500 \cdot 8 \cdot 1000}{1.5\cdot 3600} \frac{\text{kb}}{\text{s}} = 
740.74... \text{ kbps}
$$

To be sure, and have some room for error, a bitrate of 700 kbps may be suitable. This is configurable in HandBrake under the Video tab.

If you knew the run time beforehand, you could also request OBS to output the video in 700 kbps in the OBS settings, and save some time in compression. On my laptop the CPU is the bottleneck, and it maxes out all 8 cores on my Intel Core i7-8650U at 1.9GHz, and it still takes ca 50 minutes to transcode the. It takes ca 1.5GB memory, so that is not too bad. The source files are already at ca 539MB, so there is not a lot of compression to do... It is notable that I have a very weak graphics card, so hardware acceleration gets me nowhere. For someone else, that may be a halping point though.