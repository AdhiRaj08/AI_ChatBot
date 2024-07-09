import React, { useState } from 'react';
import '../App.css';
import chatbotImage from '../images (2).png';
import ChatFooter from './Chatfooter';

function Chatbot() {
  const [messages, setMessages] = useState([]);

  return (
    <>
      <div className='container'>
        <div className="panel">
          <ul>
            <img src={chatbotImage} alt="" />
            <li><a href="#">HOME</a></li>
            <li><a href="#">CHAT</a></li>
            <li><a href="#">CONTACT</a></li>
            <li><a href="#">NOTIFICATIONS</a></li>
            <li><a href="#">SETTINGS</a></li>
            <li className='logout'><a href="#">LOG OUT</a></li>
          </ul>
        </div>
        <div className="chat__mainHeader">
          <p>OPENAI CHATBOT</p>
        </div>
        <div className="message__container">
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender === 'sender' ? 'message__sender' : 'message__recipient'}>
              <p>{msg.content}</p>
            </div>
          ))}
        </div>
        <div>
          <ChatFooter messages={messages} setMessages={setMessages} />
        </div>
      </div>
    </>
  )
}

export default Chatbot;
