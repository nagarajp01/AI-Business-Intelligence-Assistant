import { Router } from "express";
import { upload } from "../middleware/multer.middleware.js";
import axios from "axios";
const router=Router()

router.route("/uploads").post(
    upload.fields([
        {
            name:"document_pdf",
            maxCount:1
        },
        {
            name:"Excel_Data_sheet",
            maxCount:1
        }
    ]),async(req,res)=>{
        console.log(req.files);
        const pdf_filepath=req.files?.document_pdf[0]?.path
        const excel_filepath=req.files?.Excel_Data_sheet[0]?.path
        if (!pdf_filepath) {
            return res.status(400).json({
                message: "PDF upload error"
            });
        }
        if (!excel_filepath) {
            return res.status(400).json({
                message: "excel sheet upload error"
            });
        }
        console.log("PDF path being sent to FastAPI:", pdf_filepath);
        console.log("Excel path being sent to FastAPI:", excel_filepath);
        const response=await axios.post("http://127.0.0.1:8000/process",{
            "document_pdf": pdf_filepath,
            "excel_file":excel_filepath,
        })
        console.log("FastAPI response received:", response.data)

        
        res.json({
            workspace_id:response.data.workspace_id,
            message:response.data.message,
        })

    }
)

export default router






