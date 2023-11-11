const axios = require("axios")

const url = "http://127.0.0.1:5000"

const defaultLang = "de"

async function recognizeEntities(sentence, language) {

    return axios
      .get(`${url}/recognize?text=${encodeURIComponent(sentence)}`)
      .then((response) => {
        console.log(
          "Response:",
          response.data
        )
        return enhanceBotEntities(response.data)
      })
      .catch((error) => {
        console.error("Error:", error)
      })
  }

function enhanceBotEntities(botResponse) {
    if (botResponse.when) {
        const today = new Date();
        if (botResponse.when.date) {
    
            const todayStrings = ["heute", "today", "oggi"];
            const tomorrowStrings = ["morgen", "tomorrow", "domani"];
            // Get today's date
            if (todayStrings.includes(botResponse.when.date?.toLowerCase())) {
                botResponse.when = "now";
            }
            else if (tomorrowStrings.includes(botResponse.when.date?.toLowerCase())) {
                // Add one day
                const tomorrow = new Date(today);
                tomorrow.setDate(tomorrow.getDate() + 1);
                botResponse.when.date = tomorrow.toISOString().slice(0,10);
            }
        }
        else if (botResponse.when.time) {
            botResponse.when.date = today.toISOString().slice(0,10)
        }
        else {
            botResponse.when = "now"
        }
    }
    botResponse.passengers = botResponse.no_of_people
    return botResponse
}


function getTextResponse(entities, language) {
    console.log("texttoresponse", entities)
    if (entities) {

        if (!language)
            language = defaultLang
    
        switch (language) {
            case "it":
                return getTextResponseIt(entities)
            case "en":
                return getTextResponseEn(entities)
            case "de":
            default:
                return getTextResponseDe(entities)
        }
    }
    else return "No entities recognized."
}


function getTextResponseDe(entities) {
    const locale = 'de-DE'
    let resp = "";
    if (entities.when === "now" || !entities.when) {
        resp += `Fahrt von ${entities.departure} nach ${entities.destination} für ${entities.passengers} Personen registriert.`;
    }
    else {
        resp = `Fahrt von ${entities.departure} nach ${entities.destination}`
        if (entities.when.date)
            resp += ` am ${formatDate(entities.when.date, locale)}`
        if (entities.when.time)
            resp += ` um ${formatTime(entities.when.time, locale)}`
        resp += ` für ${entities.passengers} Person${entities.passengers >1 ? "en" : ""} registriert.`;
    }
    resp += " Automatische Bestätigung nach 1 Minute."
    return resp

}

function formatDate(dateStr, locale) {
    // Convert the date string to a Date object
    const date = new Date(dateStr);

    // Use Intl.DateTimeFormat to format the date in German
    const formatter = new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    const localizedDate = formatter.format(date);

    return localizedDate
}

function formatTime(timeString, locale) {
    // Convert the time string to a Date object
    // Assuming the date as today for the purpose of creating a Date object
    timeString = timeString.slice(0,5)
    const date = new Date(`1970-01-01T${timeString}:00Z`);

    // Use Intl.DateTimeFormat to format the time in German
    const formatter = new Intl.DateTimeFormat(locale, {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false // Use 24-hour format
    });

    const localizedTime = formatter.format(date);

    // console.log(localizedDate);
    return localizedTime
}

  module.exports = { recognizeEntities, getTextResponse }
