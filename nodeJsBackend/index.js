const express = require("express")
const multer = require("multer")
const { audioToText } = require("./audioToText");
const { textToAudio } = require("./textToAudio");
const { mooovexQuery, mooovexRideDetails } = require("./mooovex");
const { recognizeEntities, getTextResponse } = require("./chatbot");
const fs = require('fs').promises;
const path = require('path');

const app = express()
app.use(express.json())

const storage = multer.memoryStorage(); // Use memory storage for simplicity; you can configure it to save to disk if needed
const upload = multer({ storage: storage });

app.use(express.json());


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

app.post("/ride-from-speech", upload.single("wavfile"), async (req, res) => {
    console.log("ride-from-speech called")
    const wavFile = req.file;

    // Save the WAV file to disk or process it as needed
    let paths = 'audioInputs';
    let fileName = 'recording.wav';

    const filePath = path.join(__dirname, paths, fileName);
    await fs.writeFile(filePath, wavFile.buffer);

    let recognizedText = await audioToText(paths + "/" + fileName);

    let entities;
    let cnt=3
    while (cnt++ < cnt && !entities)
        entities = await recognizeEntities(recognizedText)
    //entities = { departure: "ads", destination: "asdf", passengers: 3 }

    if (entities) {
        let textResponse = getTextResponse(entities);
    
        res.send({
            departure: entities.departure,
            destination: entities.destination,
            date: "now",
            passengers: entities.passengers,
            recognizedText: recognizedText,
            textResponse: textResponse,
            audioResponse: "uuid",
        })
    }
    else 
        res.status(401).send({error: "Could not understand voice"})
})

app.get("/get-mp3", async (req, res) => {

});

app.post("/text-to-speech", async (req, res) => {
    console.log("text to speech called for body " + JSON.stringify(req.body))
    const textInput = req.body.textInput;
    const result = await textToAudio(textInput);
    const mp3FilePath = path.join(__dirname, 'assets', 'mock-response-st-ulrich-de.mp3');

    try {
        console.log(mp3FilePath)
        const mp3Data = await fs.readFile(mp3FilePath);

        res.setHeader('Content-Type', 'audio/mpeg');

        res.send(mp3Data);
    } catch (error) {
        res.send({
            urlToAudio: result
        })
        console.error('Error reading MP3 file:', error);
        res.status(500).send('Internal Server Error');
    }
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
