const express = require("express")
const multer = require("multer")
const { audioToText } = require("./audioToText");
const { textToAudio } = require("./textToAudio");
const { mooovexQuery, mooovexRideDetails } = require("./mooovex")

const app = express()
app.use(express.json())

//const upload = multer({ storage: multer.memoryStorage() })

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

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

app.get("/", async (req, res) => {
    let result = await audioToText();
    console.log(result);
    res.send("Result: " + result);
});

app.post("/ride-from-speech",  async (req, res) => {
    console.log("ride-from-speech called")
    // todo audio to wav
    // const audioBuffer = req.file.buffer;
    // todo pass wav file or path to service
    let textResponse = await audioToText();
    // todo call Rasa or ChatGPT for entity recognition

    res.send({
        departure: "St. Ulrich",
        destination: "Klausen",
        date: "2023-11-18 14:00",
        passengers: 2,
        textResponse: textResponse,
        audioResponse: "uuid",
    })
})

app.post("/text-to-speech", async (req, res) => {
    console.log("text to speech called for " + JSON.stringify(req.body))
    // todo use real text
    const textInput = "Bitte ein Taxi von Sankt Ulrich zum Hotel Goldener Adler für zwei personen mit Skiausrüstung";
    const result = await textToAudio(textInput);
    res.send({
        urlToAudio: result
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

app.post("/mooovex-autocomplete", async (req, res) => {
    // Replace these variables with your actual values
    const query = req.query.query // Replace with your query string
    const language = req.query.language ?? "de" // Replace with 'de', 'it', or 'en'
  
    return mooovexQuery(query, language).then((results) => res.send(results))
  })
  
  app.post("/mooovex-ride", async (req, res) => {
    console.log("Starting to get ride")
  
    const body = req.body
    const language = req.query.language ?? "de"
  
    return mooovexRideDetails(
      body.origin,
      body.destination,
      body.passengers,
      body.dateObj,
      language
    ).then((result) => res.send(result))
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
