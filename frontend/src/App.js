import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ChatApp = () => {
  const [chatLog, setChatLog] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setMessageLoading] = useState(false);

  useEffect(() => {
    // Scroll to the bottom of the chat log whenever it updates
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }, [chatLog]);

  const sendQuery = async () => {
    if (userInput.trim()) {
      const newUserMessage = { type: 'user', text: userInput };
      setChatLog([...chatLog, newUserMessage]);
      try {
        setMessageLoading(true)
        const response = await axios.get(`http://localhost:8000/ask?question=${encodeURIComponent(userInput)}`);
        setMessageLoading(false)
        const systemMessage = { type: 'system', text: response.data.message };
        setChatLog([...chatLog, newUserMessage, systemMessage]);
        setTimeout(() => {
          document.getElementById('question_input').focus();
        },0);
      } catch (error) {
        console.error('Error fetching response:', error);
      }
      setUserInput('');
    }
  };

  return (
    <div className="flex flex-row h-screen">
      {/*<div className="flex flex-col bg-blue-400">
        <div className="flex flex-row bg-slate-400 p-4 text-4xl">
          <p className="flex">
            Files
          </p>

        </div>
      </div>
      */}
      <div className="flex flex-col flex-grow">
        <div className="flex flex-row bg-slate-400 p-4 text-4xl">
          <p className="flex">
            Lawdify RAG Demo
          </p>
        </div>
        <div
          id="chat-container"
          className="flex flex-col flex-grow overflow-auto p-4 space-y-2 text-xl"
        >
          {chatLog.map((message, index) => (
            <div
              key={index}
              className={
                `flex flex-row p-2 rounded-lg shrink w-4/5
                ${message.type === 'user'
                ? 'bg-blue-200 self-end'
                : 'bg-green-200 self-start'}`
              }
            >
              <p className="flex shrink font-bold">
                {message.type === 'user' ? 'User: ' : 'Agent: '}
              </p>&nbsp;
              <p className="flex shrink whitespace-pre-wrap">{message.text}</p>
            </div>
          ))}
        </div>
        <div className="p-4 border-t-2 text-xl">
          <input
            id="question_input"
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendQuery()}
            placeholder="Type your question..."
            className="w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 disabled:bg-slate-200"
            disabled={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatApp;
