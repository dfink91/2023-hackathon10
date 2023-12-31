'use client'

import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";


function RecorderJSDemo() {
  const [audioBlob, setAudioBlob] = useState(null);
  const [data, setData] = useState("")
  let gumStream = null;
  let recorder = null;
  let audioContext = null;

  useEffect(() => {
    console.log("audioBlob changed")
  }, [audioBlob])

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

  const textToSpeech = async (text) => {
    try {
      const response = await fetch('http://localhost:8080/text-to-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ textInput: text }),
      });
  
      if (!response.ok) {
        throw new Error('Failed to fetch audio');
      }
  
      const audioData = await response.arrayBuffer();
      const audioBlob = new Blob([audioData], { type: 'audio/mp3' });
      setAudioBlob(audioBlob);
    } catch (error) {
      console.error('Failed to convert text to speech:', error);
    }
  }
      

  const onStop = async (blob) => {
    console.log("uploading...");

    let data = new FormData();

    data.append("text", "this is the transcription of the audio file");
    data.append("wavfile", blob, "recording.wav");

    const config = {
      headers: { "content-type": "multipart/form-data" },
    };
    let response = await axios.post("http://localhost:8080/ride-from-speech", data, config);
    setData(response.data)
    textToSpeech(response.data.textResponse)
    console.log(response.data)
  };

  return (
    <div className="h-screen place-items-center">
      <div>
      <button className="w-16 h-8 rounded bg-blue-400 m-2" onClick={startRecording} type="button">
        Start
      </button>
      <button className="w-16 h-8 rounded bg-blue-400 m-2" onClick={stopRecording} type="button">
        Stop
      </button>

      </div>

      <div className="text-sm"><b>Start:</b> {data.departure}</div>
      <div className="text-sm"><b>Ziel:</b> {data.destination}</div>
      <div className="text-sm"><b>Personen:</b> {data.passengers}</div>
      <div className="text-sm"><b>Preis:</b> {data?.mooovexRideDetails?.price} €</div>
      <div className="text-sm"><b>Erkannter Text:</b> {data.recognizedText}</div>
      <div className="text-sm"><b>Antwort in Textform:</b> {data.textResponse}</div>


      {audioBlob && (
        <audio className="hidden" autoPlay controls onError={(e) => console.error('Audio playback error:', e)}>
<source src={URL.createObjectURL(audioBlob)} type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
      
      )}

    </div>
  );
}

export default RecorderJSDemo;
