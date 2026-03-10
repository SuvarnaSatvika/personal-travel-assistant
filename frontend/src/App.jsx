import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'

import './App.css'

function App() {
    // Greeting from the agent at beginning
    const [messages, setMessages] = useState([
        { role : 'agent', content : 'Hi there! Where would you like to travel today?'}
    ]);
    const messagesEndRef = useRef(null);
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior : "smooth"});
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);


    // inputText to remember what is currently typed in the box
    const [inputText, setInputText] = useState('');

    const [budget, setBudget] = useState('moderate');
    const [people, setPeople] = useState('2');
    const [food, setFood] = useState('Any');
    const [transportation, setTransportation] = useState('car');
    const [isThinking, setIsThinking] = useState(false);
    
    // When we hit send
    const handleSend = async () => {
        // for empty text
        if(!inputText.trim()) return;

        const userText = inputText;

        // for user's message
        const newMessages = [...messages, { role : 'user', content : inputText}];
        setMessages(newMessages);
        //clear the input box
        setInputText('');

        try{
            const response = await fetch('/api/chat', {
                method : 'POST',
                headers : {
                    'Content-Type' : 'application/json',
                },
                body : JSON.stringify({message : `[Budget: ${budget}, People: ${people}, Food: ${food}, Transportation: ${transportation}] ${userText}`}),
            });

            const data = await response.json();

            setMessages((prevMessages) => [
                ...prevMessages,
                { role : 'agent', content : data.content}
            ]);

            const downloadPDF = async (finalData) => {
                const response = await fetch('/api/generate-pdf', {
                    method: 'POST',
                    headers: { 'Content-Type' : 'application/json'},
                    body: JSON.stringify(finalData),
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "My Trip.pdf";
                document.body.appendChild(a);
                a.click();
            };
        }
        catch (error){
            console.error("Connection error: ", error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { role : 'agent', content: "Oops!!! I couldn't reach the server"}
            ]);
        }


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
                        {msg.role === 'agent' ? (
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                        ) : (msg.content)}
                    </div>
                ))}
                <div ref={messagesEndRef} />
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
