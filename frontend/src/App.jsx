import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'

import './App.css'
import Aurora from './Aurora';

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

    const downloadPDF = async (finalData) => {
            try{
                const response = await fetch('https://personal-travel-assistant.onrender.com/api/generate-pdf', {
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
            }
            catch(error){
                console.error("PDF Download Error: ", error);
            }

        };

    // inputText to remember what is currently typed in the box
    const [inputText, setInputText] = useState('');
    
    const [days, setDays] = useState('5');
    const [budget, setBudget] = useState('moderate');
    const [people, setPeople] = useState('2');
    const [food, setFood] = useState('Any');
    const [transportation, setTransportation] = useState('car');
    const [isThinking, setIsThinking] = useState(false);
    const [itineraryData, setItineraryData] = useState(null);

    // When we hit send
    const handleSend = async () => {
        // for empty text
        if(!inputText.trim()) return;

        const userMessage = inputText;
        setInputText('');

        const newMessages = [...messages, { role : 'user', content : userMessage}];
        setMessages(newMessages);

        setIsThinking(true)

        const contextMessage = `[Days: ${days}, Budget: $${budget}, People: ${people}, Food: ${food}, Transport: ${transportation}] ${userMessage}`;



        try{
            const response = await fetch('https://personal-travel-assistant.onrender.com/api/chat', {
                method : 'POST',
                headers : {
                    'Content-Type' : 'application/json',
                },
                body : JSON.stringify({message : contextMessage}),
            });

            const data = await response.json();

            if (typeof data.content === 'object'){
                setItineraryData(data.content);
                setMessages((prevMessages) => [
                ...prevMessages,
                { role : 'agent', content : "Your Itinerary is complete! Click 'DOWNLOAD ITINERARY' to download as a PDF."}
            ]);
            }
            else{
                setMessages((prevMessages) => [
                ...prevMessages,
                { role : 'agent', content : data.content}
            ]);
            }       
        }
        catch (error){
            console.error("Connection error: ", error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { role : 'agent', content: "Oops!!! I couldn't reach the server"}
            ]);
        }
        finally{
            setIsThinking(false)
        }
    };

    return(
        <div className='app-wrapper'>
            <div className='aurora-bg'>
                <Aurora
                colorStops={["#7cff67","#B19EEF","#5227FF"]}
                blend={0.5}
                amplitude={1.0}
                speed={1}
                />
            </div>
            <aside className='sidebar'>
                <h1 className='sidebar-title'>Trip Settings</h1>

                <div className='filter-group'>
                    <label>Number of Days</label>
                    <input type="number" value = {days} onChange={(e) => setDays(e.target.value)}></input>
                </div>

                <div className='filter-group'>
                    <label>Budget</label>
                    <select value = {budget} onChange={(e) => setBudget(e.target.value)}>
                        <option>Low</option>
                        <option>moderate</option>
                        <option>High</option>
                    </select>
                </div>

                <div className='filter-group'>
                    <label>Number of People</label>
                    <input type="number" value = {people} onChange={(e) => setPeople(e.target.value)}></input>
                </div>

                <div className='filter-group'>
                    <label>Food Preference</label>
                    <select value = {food} onChange={(e) => setFood(e.target.value)}>
                        <option>No preference</option>
                        <option>Vegetarian</option>
                        <option>Vegan</option>
                        <option>Halal</option>
                    </select>
                </div>

                <div className='filter-group'>
                    <label>Mode of Transportation</label>
                    <select value = {transportation} onChange={(e) => setTransportation(e.target.value)}>
                        <option>No preference</option>
                        <option>Public Transit</option>
                        <option>Car</option>
                    </select>
                </div>

                <button className='pdf-btn' onClick={() => {
                    if (itineraryData){
                        downloadPDF(itineraryData)
                    }
                    else{
                        alert("Please finish planning your itinerary and type 'finalize' to get the pdf ready")
                    }
                }}>
                    Download Itinerary</button>
            </aside>

            <main className='main-chat'>
                <div className='chat-window'>

                    <div className="welcome-banner">
                        <h2>✈️ AI Travel Guide</h2>
                        <p>Set your budget, group size, and preferences on the left. Chat with your agent to build the perfect trip, and type <strong>"finalize"</strong> when you are ready to generate your PDF itinerary!</p>
                    </div>

                    {messages.map((msg, index) => (
                        <div key = {index} className={`message ${msg.role}`}>
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                    ))}

                    {isThinking && (
                        <div className='thinking-animation'>
                            ✈️🍕🧳🚗
                        </div>
                    )}
                    <div ref={messagesEndRef}></div>
                </div>
                    <div className='input-area'>
                        <input 
                        value = {inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        placeholder='Ask your agent anything...'
                        />
                        <button onClick={handleSend}>Send</button>
                    </div>
            </main>
        </div>
    )
}

export default App
