const fs = require('fs');

const textToSpeech = require('@google-cloud/text-to-speech');
const util = require('util');

const textToAudio = async (text) => {
    console.log("Text to audio service for: " + text);
    const keyFile = process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON ? JSON.parse(process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON) : null;

    if (!keyFile) {
        console.log("No key file")
        let fileURL = "nodeJsBackend/assets/mock-text-to-speech.mp3"
        return { audioFileURL: fileURL }
    }

    const client = new textToSpeech.TextToSpeechClient(
        {
            credentials: {
                client_email: keyFile.client_email,
                private_key: keyFile.private_key,
            }
        }
    );

    const request = {
        input: { text: text },
        voice: { languageCode: 'de-DE', ssmlGender: 'NEUTRAL' },
        audioConfig: { audioEncoding: 'MP3' },
    };

    const [response] = await client.synthesizeSpeech(request);
    const writeFile = util.promisify(fs.writeFile);
    let filePath = 'generatedAudio/production-text-to-speech.mp3';
    console.log("Writing file " + filePath);
    await writeFile(filePath, response.audioContent, 'binary');
    console.log('Audio content written to file: output.mp3');
    // todo upload
    let fileURL = filePath;
    return { audioFileURL: fileURL }
}

module.exports = { textToAudio };