"use client"

import React, { useEffect, useMemo } from "react"

export default function Home() {
  const msg = useMemo(() => {
    const speechMsg = new SpeechSynthesisUtterance()
    speechMsg.text = "Here is your itenerary for Ortisei, Italy."
    return speechMsg
  }, [])

  // useEffect(() => {
  //   window.speechSynthesis.speak(msg);
  // }, [msg]);

  return (
    <div className="App">
      <h1>React Text to Speech App</h1>
    </div>
  )
}
