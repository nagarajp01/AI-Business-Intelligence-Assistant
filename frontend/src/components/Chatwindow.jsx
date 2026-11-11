import { useState } from "react";
import "../styles/Chat.css";
// import axios from "axios";

function Chatwindow({workspaceId}){
    const[messages,setMessages]=useState([]);
    const[input,setInput]=useState("");
    const[loading,setLoading]=useState(false);

    const handleSubmit= async(e)=>{
        e.preventDefault()
        if(!input.trim()){
            return
        }
        const question=input.trim()
        setMessages(prev=>[...prev,
            {
                sender:"user",
                text:question
            }])
            setInput("")
            setLoading(true)
            try {
                    // const response=await axios.post("http://localhost:5000/api/ask",{
                    // question:question,
                    // workspace_id:workspaceId});
                const response=await fetch("http://localhost:5000/api/ask",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                    },
                    body:JSON.stringify({
                        question:question,
                        workspace_id:workspaceId
                    })
                });
            // setMessages(prev => [...prev,{
            //     sender:"ai",
            //     text:response.data.answer}])
            //below for streaming ui reponse of ai message , above also works
                if (!response.ok) {
                    throw new Error("Failed to get AI response");
                }
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                setMessages(prev => [...prev, {
                    sender: "ai",
                    text: ""
                }]);
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        break;
                    }
                    const chunk = decoder.decode(value, { stream: true });
                    setMessages(prev => {
                        const updatedMessages = [...prev];
                        updatedMessages[updatedMessages.length - 1] = {
                            ...updatedMessages[updatedMessages.length - 1],
                            text: updatedMessages[updatedMessages.length - 1].text + chunk
                        };
                        return updatedMessages;
                    });
                }
            } catch (error) {
                setMessages(prev=>[...prev,
                    {
                        sender:"ai",
                        text:"Something Went wrong. Please try again"
                    }
                ])
                
            }
            finally {
                 setLoading(false)
            }
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
                    <div className={msg.sender==="user"?"user-message" : "ai-message"} key={index}>
                        <p>{msg.text}</p>
                        {msg.sender==="ai" && 
                        typeof msg.text === "string" && msg.text.includes("BusinessFileReport.pdf")&&
                        workspaceId && (
                            <a  href={`http://localhost:5000/api/download-report/${workspaceId}`}
                            download="BusinessFileReport.pdf">Download PDF Report</a>
                        )}
                    </div>
                ))
               }
               {/* {
                loading && (
                    <div className="ai-message">
                        <p>Thinking.....</p>
                    </div>
                )
               } */}
               {
               loading && (
                messages[messages.length - 1]?.sender !== "ai" ||
                !messages[messages.length - 1]?.text) && (
                <div className="ai-message">
                    <p>Thinking...</p>
                </div>
            )}
            </div>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Ask Anything about your business data...."
                value={input} onChange={(e)=> setInput(e.target.value)}/>
                <button type="submit" disabled={loading}>
                    {
                        loading ? "Sending..." : "Send" 
                    }
                </button>
            </form>
        </div>
    )
}


export default Chatwindow;