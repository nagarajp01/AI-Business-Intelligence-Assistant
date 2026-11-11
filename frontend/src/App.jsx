import Sidebar from "./components/Sidebar"
import  ChatWindow from "./components/Chatwindow"
import './App.css'
import { useState } from "react";


function App() {
   const[darkmode,setDarkMode]=useState(false);
   const [workspaceId,setWorkspaceId]=useState(null)
  return(
    <div className={`app ${darkmode ? "dark-theme" : "light-theme"}`}>
      <Sidebar darkmode={darkmode} setDarkMode={setDarkMode} workspaceId={workspaceId} setWorkspaceId={setWorkspaceId} />
      <ChatWindow workspaceId={workspaceId} />
    </div>
  )
}

export default App
