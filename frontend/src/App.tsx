import React from "react";
import MicStream from "./MicStream";

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-8">🎤 Speech-to-Text Stream</h1>
      <MicStream />
    </div>
  );
}

export default App;
