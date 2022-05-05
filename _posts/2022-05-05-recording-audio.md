---
title:  "Recording Audio for Machine Learning with PyAudio"
tags: [machine learning, python, pyaudio]
---

In a PhD course I am taking, we use Hidden Markov Models for speech recognition.
To make it more exciting, we are encouraged to collect our own training and test data sets.
It is a good exercise, and it makes you think about organization of data, metadata collection and more.

To collect audio data, I use my laptop, running Python. I use the [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) library.

The hard part in using PyAudio for recording is that most code examples use the synchronous -- blocking -- API of PyAudio. It means that you cannot easily stop an ongoing recording. Two variants are common on the internet. Either, you set a fixed recording time in the start [link](https://people.csail.mit.edu/hubert/pyaudio/docs/#example-blocking-mode-audio-i-o) or you use a third party library that can accept user input in a separate thread and signal PyAudio running in the main thread [link](https://stackoverflow.com/a/62627665/4050510). I think both alternatives are bad.

The design requirements that I had in mind were

1. **No extra libraries.** Maybe other libraries are needed to do machine learning, but the actual sound recording should be fixed by a PyAudio and standard libraries.

1. **Reliable threading.** PyAudio runs the callbacks in a separate thread. Some snippets on StackOverflow use `global` to allow synchronization of data between threads, but that is error prone. So no global variables. I use standard python thread safe objects such as `threading.Event` and `queue.SimpleQueue`.

1. **Low latency.** One simple solution is to restart PyAudio every time you want to record something. However, there is significant overhead in creating audio streams in PyAudio, so we should reuse a stream whenever we can. Otherwise, there can be delays from pressing "start recording" to actual start of recording of several 100s of milliseconds. For short audio clips, this matters.

One solution that fulfils these requirements is the code below. It is written to be understandable on its own. I hope you find it useful.

<script src="https://gist.github.com/el-hult/9bafd3b4cb0ddff6dd00c0b960b83378.js"></script>