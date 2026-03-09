import { useState } from 'react'

import './App.css'

function App() {
    // Greeting from the agent at beginning
    const [messages, setMessages] = useState([
        { role : 'agent', content : 'Hi there! Where would you like to travel today?'}
    ]);

    // inputText to remember what is currently typed in the box
    const [inputText, setInputText] = useState('');

    // When we hit send
    const handleSend = () => {
        // for empty text
        if(!inputText.trim()) return;
        // for user's message
        const newMessages = [...messages, { role : 'user', content : inputText}];
        setMessages(newMessages);
        //clear the input box
        setInputText('');
    };

    return(
        <div className="chat-container">
            <header className='chat-header'>
                <h1>AI Travel Agent</h1>
                <p>Plan your next adventure</p>
            </header>

            <div className='chat-window'>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        <strong>{msg.role === 'user' ? 'You: ' : 'Agent: '}</strong>
                        {msg.content}
                    </div>
                ))}
            </div>
        

            {/* The Input Box */}
            <div className='input-area'>
                <input 
                    type = "text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={(e) => e.key ==='Enter' && handleSend()}
                    placeholder='Type a message...'
                    />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    )
}

export default App
