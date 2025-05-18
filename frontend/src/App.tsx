import React, { useEffect, useState } from 'react'

const App = () => {
  const [status, setStatus] = useState("initializing...")

  useEffect(() => {
    const ping = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/health`)
        const json = await res.json()
        setStatus(json.message || "connected")
      } catch {
        setStatus("connection failed")
      }
    }

    ping()
  }, [])

  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center space-y-4 p-8">
      <h1 className="text-4xl sm:text-5xl font-bold text-cyan-400 animate-pulse">
        🧠 SoulEngine Mandala
      </h1>
      <p className="text-gray-300 text-lg">PWA-powered Construct Visualizer</p>
      <p className="text-sm text-emerald-400 bg-black/30 px-3 py-1 rounded-md">
        Status: {status}
      </p>
    </div>
  )
}

export default App