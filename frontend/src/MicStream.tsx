import React, { useRef, useState } from "react";

const MicStream: React.FC = () => {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const wsRef = useRef<WebSocket | null>(null);
  const processorRef = useRef<AudioWorkletNode | null>(null);

  const startRecording = async () => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket opened");
      setRecording(true);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      setRecording(false);
    };

    ws.onmessage = (event) => {
      const text = event.data;
      console.log("Received WS message:", text);
      if (text.trim()) {
        setTranscript((prev) => prev + " " + text);
      }
    };

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioContext = new AudioContext({ sampleRate: 16000 });
    const source = audioContext.createMediaStreamSource(stream);

    await audioContext.audioWorklet.addModule("/worklet-processor.js");

    const processor = new AudioWorkletNode(audioContext, "pcm-processor");
    processor.port.onmessage = (event) => {
      const chunk: ArrayBuffer = event.data;
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(chunk);
      }
    };

    source.connect(processor).connect(audioContext.destination);

    processorRef.current = processor;
  };

  const stopRecording = () => {
    setRecording(false);
    wsRef.current?.close();
    processorRef.current?.disconnect();
  };

  const resetTranscript = () => {
    setTranscript("");
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <button
        onClick={recording ? stopRecording : startRecording}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      <button
        onClick={resetTranscript}
        className="bg-gray-500 text-white px-4 py-2 rounded"
      >
        Clear Transcript
      </button>

      <div className="mt-4 p-4 border rounded w-full max-w-lg bg-white">
        <h2 className="text-lg font-bold mb-2">Live Transcription:</h2>
        <p className="whitespace-pre-wrap">{transcript || "..."}</p>
      </div>
    </div>
  );
};

export default MicStream;
