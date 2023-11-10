const express = require("express")
const multer = require("multer")

const app = express()
const upload = multer({ storage: multer.memoryStorage() })

app.listen(8080, () => {
  console.log("Starting to listen on port 8080")
})

app.get("/", (req, res) => {
  console.log("Hello backend")
  return res.send({ x: "Hello Hackathon1010" })
})

app.post("/", (req, res) => {
  console.log("Hello backend post")
  return res.send("Hello Hackathon1010 post")
})

app.post("/ride-from-speech", upload.single("audio"), async (req, res) => {
  console.log("transcribeWhisper called")
  res.send({
    departure: "St. Ulrich",
    destination: "Klausen",
    date: "2023-11-18 14:00",
    passengers: 2,
    textResponse: "Fahrt von St. Ul",
    audioResponse: "uuid",
  })
})

app.get("/audio-response", (req, res) => {
  console.log("Hello backend")
  return res.send("bo") // TODO return an audio file for frontend
})

app.post("save-ride-to-mooovex", async (req, res) => {
  req.body = {
    departure: "St. Ulrich",
    destination: "Klausen",
    date: "2023-11-18 14:00",
    passengers: 2,
    textResponse: "",
    audioResponse: "uuid",
  }

  // TODO Save ride to movex
  return res.send({ mooovexId: "mId" })
})

async function transcribeAudioWithWhisper(audioFile) {
  return "This will be transcribed text"
  // const apiKey = ""; // Replace with your actual API key
  // const endpoint = "https://api.openai.com/v1/whisper-transcribe"; // Replace with the actual Whisper API endpoint

  // let formData = new FormData();
  // formData.append("file", audioFile);

  // try {
  //   const response = await fetch(endpoint, {
  //     method: "POST",
  //     headers: {
  //       Authorization: `Bearer ${apiKey}`,
  //       // Add other necessary headers
  //     },
  //     body: formData,
  //   });

  //   const data = await response.json();
  //   return data.transcription; // Or however the response is structured
  // } catch (error) {
  //   console.error("Error transcribing audio:", error);
  // }
}
