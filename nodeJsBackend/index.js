const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

app.listen(8080, () => {
  console.log("Starting to listen on port 8080");
});

app.get("/", (req, res) => {
  console.log("Hello backend");
  res.send("Hello Hackathon1010");
});

app.post("/transcribeWhisper", upload.single("audio"), (req, res) => {
  const audioBuffer = req.file.buffer;

  // Save the buffer to a temporary file or directly stream it to Whisper
  // For simplicity, let's assume we're directly passing the buffer to a Whisper process

  const whisper = spawn("whisper", ["--", "-"]);

  whisper.stdin.write(audioBuffer);
  whisper.stdin.end();

  let transcription = "";
  whisper.stdout.on("data", (data) => {
    transcription += data.toString();
  });

  whisper.on("close", () => {
    res.send({ transcription });
  });
});
