import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    const res = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="min-h-screen bg-gray-800 flex items-center justify-center px-4">
      <div className="bg-gray-600 shadow-xl rounded-xl p-6 w-full max-w-2xl">
        <h1 className="text-2xl font-bold text-yellow-400 mb-4 text-center">
          LawCraftsMan
        </h1>

        <textarea
          className="w-full h-32 p-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400 mb-4 resize-none text-cyan-50"
          placeholder="Type your legal question here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <div className="flex justify-center">
          <button
            className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-2 px-6 rounded-full transition-all duration-300"
            onClick={sendMessage}
          >
            Ask
          </button>
        </div>

        {response && (
          <div className="mt-6 bg-gray-800 border border-gray-200 p-4 rounded-md text-yellow-200">
            <p className="font-medium mb-1">Response:</p>
            <p>{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
