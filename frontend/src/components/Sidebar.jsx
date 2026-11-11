import "../styles/Sidebar.css";
import { useState, useRef } from "react";


function Sidebar({darkmode,setDarkMode,workspaceId,setWorkspaceId}){

    const[collapsed,setCollapsed]=useState(false);
    const[pdfFile,setPdfFile]=useState(null);
    const[excelFile,setExcelFile]=useState(null)
    const [uploading, setUploading] = useState(false);
    const pdfInputRef=useRef(null)
    const excelInputRef=useRef(null)
    
    const uploadFiles=async(pdf,excel)=>{
        if (!pdf || !excel) {
            console.log("Please select both files");
            return;
        }
        const formData=new FormData();
        formData.append("document_pdf",pdf);
        formData.append("Excel_Data_sheet",excel);
        try {
            setUploading(true)
            const response=await fetch("http://localhost:5000/api/uploads",{
                method:"POST",
                body:formData
            });
            if(!response.ok){
                throw new Error("File upload failed")
            }
            const data= await response.json();
            if (!data.workspace_id) {
                throw new Error("Workspace ID not received from backend");
            }
            setWorkspaceId(data.workspace_id);
            console.log("Workspace_id: ", data.workspace_id)
        } catch (error) {
            console.error("Upload error: ",error)
            
        }finally{
            setUploading(false)
        }


    }
   
    const handleUploadClick=()=>{
        pdfInputRef.current.click()
    };
    const handleExcelClick = () => {
    excelInputRef.current.click();
    };
    const handlePdfChange=(e)=>{
        const file=e.target.files[0];
        if (file){
            setPdfFile(file);
            console.log("Selected PDF: ", file)
            // excelInputRef.current.click();
        }
        
    };
    const handleExcelChange=(e)=>{
        const file=e.target.files[0];
        if(file){
            setExcelFile(file)
            console.log("Selected Excel: ",file);
            uploadFiles(pdfFile,file)
        }
    }

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
                    <button onClick={handleUploadClick} disabled={uploading}>
                        Select PDF
                    </button>
                    {pdfFile && (
                        <div>
                            <p>PDF: {pdfFile.name}</p>
                            <button onClick={handleExcelClick} disabled={uploading}>
                                Select Excel
                            </button>
                        </div>
                    )}
                    {excelFile && <p>Excel: {excelFile.name}</p>}
                    {uploading && <p>Uploading documents....</p>}
                    {workspaceId && !uploading && (<p>Documents uploaded Successfully!</p>)}
                    <input 
                    type="file"
                    accept=".pdf"
                    ref={pdfInputRef}
                    onChange={handlePdfChange}
                    hidden
                    />
                    <input
                     type="file"
                     accept=".xlsx,.xls,.csv"
                     ref={excelInputRef}
                     onChange={handleExcelChange}
                     hidden
                    />

                </div>
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