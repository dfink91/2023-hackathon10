// todo enable here and set ENV variable for API KEY
const enableGoogleSTT = false;
const keyFilePath = '/Users/lukas/IdeaProjects/NoiHack23/noihackathon23-bcc9300070d9.json';
const fs = require('fs');
const keyFile = JSON.parse(fs.readFileSync(keyFilePath));

const speech = require('@google-cloud/speech');

const client = new speech.SpeechClient({
    credentials: {
        client_email: keyFile.client_email,
        private_key: keyFile.private_key,
    },
});

const processGoogleSTT = async () => {
    if (!enableGoogleSTT){
        return "bitte ein Taxi von St Ulrich zum Hotel Goldener Adler für zwei Personen mit Skiausrüstung (MOCK)";
    }
    const fileName = 'assets/mock-request-taxi-sankt-ulrich-goldener-adler2.wav'; // Replace with the path to your WAV file

    // Reads the audio file into memory
    const file = fs.readFileSync(fileName);
    const audioBytes = file.toString('base64');

    // The audio file's encoding, sample rate, and language
    const audio = {
        content: audioBytes,
    };

    const config = {
        encoding: 'LINEAR32',
        //sampleRateHertz: 16000,
        languageCode: 'de-DE',
    };
    const request = {
        audio: audio,
        config: config,
    };

    // Detects speech in the audio file
    const [response] = await client.recognize(request);
    console.log(JSON.stringify(response));
    const transcription = response.results
        .map(result => result.alternatives[0].transcript)
        .join('\n');

    return transcription;
}

module.exports = { processGoogleSTT };