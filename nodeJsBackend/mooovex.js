const axios = require("axios")

const region = "Südtirol"
const defaultLang = "de"
const KEY_PLACE_ID = "google_place_id"

async function mooovexQuery(query, language) {
  return axios
    .post("https://dev.api.mooovex.com/hackathon/autocomplete", {
      query: query + region,
      language: language ?? defaultLang,
    })
    .then(function (response) {
      console.log(
        "Response:",
        response.data.map((r) => `${r.name}, ${r.formatted_address}`)
      )
      return response.data[0]
    })
    .catch(function (error) {
      console.error("Error:", error)
    })
}

// {
//     origin_google_place_id: string;
//     destination_google_place_id: string;
//     passenger_count: number; // int, >= 1, <= 8
//     when:
//       | "now"
//       | {
//           date: string; // yyyy-mm-dd
//           time: string; // hh:mm:ss
//         };
//     language: "de" | "it" | "en";
//   }

async function mooovexRideDetailsRequest(originId, destinationId, passengers, dateObj, language) {
  console.log(originId, destinationId, passengers, dateObj)
  if (!(dateObj.date && dateObj.time)) dateObj = "now"

  return axios
    .post("https://dev.api.mooovex.com/hackathon/routedetails", {
      origin_google_place_id: originId,
      destination_google_place_id: destinationId,
      passenger_count: passengers,
      when: dateObj,
      language: language ?? defaultLang,
    })
    .then(function (response) {
      console.log("Response:", response.data)
      return response.data
    })
    .catch(function (error) {
      console.error("Error:", error)
    })
}

async function mooovexRideDetails(originStr, destinationStr, passengers, dateObj, language) {
  return Promise.all([
    mooovexQuery(originStr, language),
    mooovexQuery(destinationStr, language),
  ]).then(([origObj, destObj]) => {
    return mooovexRideDetailsRequest(
      origObj[KEY_PLACE_ID],
      destObj[KEY_PLACE_ID],
      passengers,
      dateObj,
      language
    )
  })
}

module.exports = { mooovexQuery, mooovexRideDetails, mooovexRideDetailsRequest }
