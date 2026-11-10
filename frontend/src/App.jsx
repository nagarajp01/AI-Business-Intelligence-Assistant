import Sidebar from "./components/Sidebar"
import  ChatWindow from "./components/Chatwindow"
import './App.css'
import { useState } from "react";


function App() {
   const[darkmode,setDarkMode]=useState(false);
  return(
    <div className={`app ${darkmode ? "dark-theme" : "light-theme"}`}>
      <Sidebar darkmode={darkmode} setDarkMode={setDarkMode} />
      <ChatWindow />
    </div>
  )
}

export default App
