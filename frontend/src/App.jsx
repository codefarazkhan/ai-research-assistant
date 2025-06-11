import  { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    await axios.post('http://localhost:8000/upload', formData);
    alert('File uploaded');
  };

  const handleAsk = async () => {
    const res = await axios.get(`http://localhost:8000/ask?q=${question}`);
    setAnswer(res.data.answer);
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">AI PDF Q&A Assistant</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="bg-blue-500 text-white p-2 m-2 rounded">Upload</button>
      <br />
      <input
        className="border p-2 w-96"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleAsk} className="bg-green-500 text-white p-2 m-2 rounded">Ask</button>
      <div className="mt-4">
        <strong>Answer:</strong>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default App;
