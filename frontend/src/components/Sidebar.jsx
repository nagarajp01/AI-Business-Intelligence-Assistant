
// import {
//   PanelLeftClose,
//   PanelLeftOpen,
//   Plus,
//   FileText,
//   FileSpreadsheet,
//   Upload,
//   Sun,
//   Moon,
//   BrainCircuit
// } from "lucide-react";

import "../styles/Sidebar.css";
import { useState } from "react";


function Sidebar({darkmode,setDarkMode}){

    const[collapsed,setCollapsed]=useState(false);
   

    const toggleSidebar=()=>{
        setCollapsed(!collapsed);
    }
    const toggleTheme=()=>{
        setDarkMode(!darkmode)
    }



    return(
       <div >
         <aside className={collapsed ? "sidebar collapsed" : "sidebar"}>
            <div className="sidebar-header">
                <h3>BI ASSISTANT</h3>
                <button onClick={toggleSidebar}>
                    {collapsed ? "Open" : "Close"}
                </button>
            </div>
            {!collapsed && (
            <div>
                <button>New Chat</button>
                <div className="uploaded_documents">
                    <span>file name pdf</span>
                    <span>file name excel</span>
                </div>
                <button>Upload Documents</button>
                <button onClick={toggleTheme}>
                    {darkmode ? "light-mode" : "dark-mode"}
                </button>
            </div>
            
            )}

        </aside>
       </div>
    )
}

export default Sidebar;