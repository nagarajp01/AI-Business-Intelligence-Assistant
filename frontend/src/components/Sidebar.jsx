import "../styles/Sidebar.css";
import { useState, useRef } from "react";


function Sidebar({darkmode,setDarkMode,workspaceId,setWorkspaceId}){

    const[collapsed,setCollapsed]=useState(false);
    const[pdfFile,setPdfFile]=useState(null);
    const[excelFile,setExcelFile]=useState(null)
    const[uploading, setUploading] = useState(false);
    const[uploadError, setUploadError] = useState("");

    const pdfInputRef=useRef(null)
    const excelInputRef=useRef(null)
    
    // Upload selected files
    const uploadFiles=async()=>{
        if (!pdfFile && !excelFile) {
           setUploadError("Please select at least one file (PDF or Excel).");
           return;
        }
        const formData=new FormData();
        // formData.append("document_pdf",pdf);
        // formData.append("Excel_Data_sheet",excel);
        if (pdfFile){
            formData.append("document_pdf",pdfFile);
        }
        if(excelFile){
            formData.append("Excel_Data_sheet",excelFile)
        }
        try {
            setUploading(true)
            setUploadError("");
            setWorkspaceId(null)
            const response=await fetch("http://localhost:5000/api/uploads",{
                method:"POST",
                body:formData
            });
            const data= await response.json();
            if(!response.ok){
                throw new Error(data.message || "File upload failed")
            }
            if (!data.workspace_id) {
                throw new Error("Workspace ID not received from backend");
            }
            setWorkspaceId(data.workspace_id);
            console.log("Workspace_id: ", data.workspace_id)
        } catch (error) {
            console.error("Upload error: ",error);
            setWorkspaceId(null);
            setUploadError(error.message || "Failed to upload documents. Please try again.")
        }finally{
            setUploading(false)
        }


    };
    // Open PDF file selector
    const handleUploadClick=()=>{
        pdfInputRef.current.click()
    };
    // Open Excel file selector
    const handleExcelClick = () => {
        excelInputRef.current.click();
    };
    // Handle PDF selection
    const handlePdfChange=(e)=>{
        const file=e.target.files[0];
        if (file){
            setPdfFile(file);
            setWorkspaceId(null);
            setUploadError("")
            // setExcelFile(null);
            console.log("Selected PDF: ", file)
        }
        e.target.value="";
    };
    // Handle Excel selection
    const handleExcelChange=(e)=>{
        const file=e.target.files[0];
        if(file){
            setExcelFile(file);
            setWorkspaceId(null);
            setUploadError("");
            console.log("Selected Excel: ",file);
            // uploadFiles(pdfFile,file)
        }
        e.target.value="";
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
                <p>
                    Upload a PDF document, an Excel file, or both to get AI-powered business insights.
                </p>
                <div className="uploaded_documents">
                    <button onClick={handleUploadClick} disabled={uploading}>
                        Select PDF File
                    </button>
                    <button onClick={handleExcelClick} disabled={uploading}>
                        Select Excel File
                    </button>
                    {pdfFile && (
                            <p>PDF: {pdfFile.name}</p>
                    )}
                    {excelFile && (
                        <p>Excel: {excelFile.name}</p>
                    )}
                    <button onClick={uploadFiles} disabled={uploading || (!pdfFile && !excelFile)}>
                        {uploading ? "Uploading..." : "Upload Files"}
                    </button>

                    {uploading && (
                        <p>Processing files...</p>
                    )}
                    {uploadError && (
                        <p className="upload-error">{uploadError}</p>
                    )}
                    {workspaceId && !uploading && (<p>Files uploaded successfully! Your workspace is ready.</p>)}
                    <input 
                    type="file"
                    accept=".pdf"
                    ref={pdfInputRef}
                    onChange={handlePdfChange}
                    hidden
                    />
                    <input
                     type="file"
                     accept=".xlsx,.xls"
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