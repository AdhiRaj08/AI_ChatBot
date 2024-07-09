import React, { useState } from 'react';

const Chatfooter = ({ messages, setMessages }) => {
  const [msg, setMsg] = useState('');

  const setPrint = (msgContent, senderType) => {
    const newMessage = {
      content: msgContent,
      sender: senderType
    };
    setMessages(prevMessages => [newMessage, ...prevMessages]);
  };
  

  const handleSendMessage = async (e) => {
    e.preventDefault();
  
    try {
      // Call the API to get the response
      const response = await fetch('http://localhost:5000/generate-response', {
        method: 'POST',
        mode: 'cors',  // Enable CORS mode
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: msg }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      
      const data = await response.json();
      
  
      // Set the response from the API as recipient's message
      setPrint(msg, 'sender');
      setPrint(data.response, 'recipient');
      
      setMsg('');
      
    } catch (error) {
      console.error('Fetch Error:', error);
    }
  };
  

  return (
    <div className="chat__footer">
      <form className="form" onSubmit={handleSendMessage}>
        <input
          type="text"
          placeholder="Write message"
          className="message"
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
        />
        <button className="sendBtn">SEND</button>
      </form>
    </div>
  );
};

export default Chatfooter;
