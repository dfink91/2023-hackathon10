const fs = require('fs');
const enableTextToAudio = false;

const textToSpeech = require('@google-cloud/text-to-speech');
const util = require('util');

const textToAudio = async (text) => {
    if (!enableTextToAudio) {
        let fileURL = "https://www.dropbox.com/scl/fi/nttzxj4wgy9rqk0bkej5w/mock-text-to-speech.mp3?rlkey=m8cyoxfy8ita0jqs8qj9qn69n&dl=0"
        return { audioFileURL: fileURL }
    }

    // todo env variable
    const keyFilePath = '/Users/lukas/IdeaProjects/NoiHack23/noihackathon23-bcc9300070d9.json';
    const keyFile = JSON.parse(fs.readFileSync(keyFilePath));

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
    let filePath = '/Users/lukas/IdeaProjects/NoiHack23/output.mp3';
    await writeFile(filePath, response.audioContent, 'binary');
    console.log('Audio content written to file: output.mp3');
    // todo upload
    let fileURL = filePath;
    return { audioFileURL: fileURL }
}

module.exports = { textToAudio };