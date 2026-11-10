import { useState } from "react";
import "../styles/Chat.css";

function Chatwindow(){
    const[messages,setMessages]=useState([]);
    const[input,setInput]=useState("");

    const handleSubmit=(e)=>{
        e.preventDefault()
        if(!input.trim()){
            return
        }
        setMessages([...messages,input])
        setInput("")
    }
    return(
        <div className="chat-window">
            <header>
                <h2>AI-Business Intelligence Assistant</h2>
            </header>
           {messages.length==0 && (
             <section>
                <h2>Welcome to AI Business Intelligence Assistant</h2>
                <p>Upload your PDF and Excel files, then ask questions to get business insights.</p>
            </section>
           )}
            <div className="chat-messages">
               {
                messages.map((msg,index)=>(
                    <div className="user-message" key={index}>
                        <p>{msg}</p>
                    </div>
                ))
               }
            </div>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Ask Anything about your business data...."
                value={input} onChange={(e)=> setInput(e.target.value)}/>
                <button type="submit">Send</button>
            </form>
        </div>
    )
}


export default Chatwindow;