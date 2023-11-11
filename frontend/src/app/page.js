'use client'

import React from "react";
import axios from "axios";

function RecorderJSDemo() {
  let gumStream = null;
  let recorder = null;
  let audioContext = null;

  const startRecording = () => {
    let constraints = {
      audio: true,
      video: false,
    };

    audioContext = new window.AudioContext();
    console.log("sample rate: " + audioContext.sampleRate);

    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function (stream) {
        console.log("initializing MediaRecorder ...");

        gumStream = stream;

        recorder = new MediaRecorder(stream);

        let chunks = [];

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            chunks.push(event.data);
          }
        };

        recorder.onstop = () => {
          const blob = new Blob(chunks, { type: "audio/wav" });
          onStop(blob);
        };

        recorder.start();
        console.log("Recording started");
      })
      .catch(function (err) {
        console.log(err);
        // enable the record button if getUserMedia() fails
      });
  };

  const stopRecording = () => {
    console.log("stopButton clicked");

    if (recorder) {
      recorder.stop(); // stop microphone access
      gumStream.getAudioTracks()[0].stop();
    }
  };

  const onStop = (blob) => {
    console.log("uploading...");

    let data = new FormData();

    data.append("text", "this is the transcription of the audio file");
    data.append("wavfile", blob, "recording.wav");

    const config = {
      headers: { "content-type": "multipart/form-data" },
    };
    axios.post("http://localhost:8080/ride-from-speech", data, config);
  };

  return (
    <div>
      <button onClick={startRecording} type="button">
        Start
      </button>
      <button onClick={stopRecording} type="button">
        Stop
      </button>
    </div>
  );
}

export default RecorderJSDemo;
