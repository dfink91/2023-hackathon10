const { getTextResponse } = require("./chatbot");


console.log(getTextResponse({departure: "Ortisei", destination: 'Bozen', passengers: 2}, "de"));
console.log(getTextResponse({departure: "Ortisei", destination: 'Bozen', passengers: 2, when: {date: "2023-11-18", time:"15:00"}}, "de"));
console.log(getTextResponse({departure: "Ortisei", destination: 'Bozen', passengers: 1, when: {date: "2023-11-18", time:"15:00"}}, "de"));