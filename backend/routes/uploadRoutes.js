import { Router } from "express";
import { upload } from "../middleware/multer.middleware.js";
import axios from "axios";
const router=Router()


router.route("/uploads").post(
    (req, res, next) => {
        upload.fields([
            {
                name: "document_pdf",
                maxCount: 1
            },
            {
                name: "Excel_Data_sheet",
                maxCount: 1
            }
        ])(req, res, (error) => {
            if (error) {
                if (error.code === "LIMIT_FILE_SIZE") {
                    return res.status(413).json({
                        message: "File size exceeds the 20 MB limit."
                    });
                }
                return res.status(400).json({
                    message: "File upload failed",
                    error: error.message
                });
            }
            next();

        });
    },
    async (req, res) => {
        try {
            const pdf_filepath = req.files?.document_pdf?.[0]?.path;
            const excel_filepath = req.files?.Excel_Data_sheet?.[0]?.path;

            if (!pdf_filepath || !excel_filepath) {
                return res.status(400).json({
                    message: "Both a PDF document and an Excel file are required."
                });
            }
            if (!pdf_filepath.toLowerCase().endsWith(".pdf")) {
                return res.status(400).json({
                    message: "The document must be a PDF file."
                });
            }
            if (
                !excel_filepath.toLowerCase().endsWith(".xlsx") &&
                !excel_filepath.toLowerCase().endsWith(".xls")
            ) {
                return res.status(400).json({
                    message: "The data sheet must be an Excel file (.xlsx or .xls)."
                });
            }

            const response = await axios.post(
                "http://127.0.0.1:8000/process",
                {
                    document_pdf: pdf_filepath,
                    excel_file: excel_filepath
                },
                {
                    timeout: 600000
                }
            );

            return res.status(200).json({
                workspace_id: response.data.workspace_id,
                message: response.data.message
            });

        } catch (error) {
            console.error(
                "File processing failed:",
                error.response?.data || error.message
            );

            if (error.code === "ECONNREFUSED") {
                return res.status(503).json({
                    message: "AI service is unavailable. Please try again later."
                });
            }

            if (error.code === "ECONNABORTED") {
                return res.status(504).json({
                    message: "AI processing timed out. Please try again."
                });
            }

            if (error.response) {
                return res.status(error.response.status).json({
                    message:
                    error.response.data?.detail ||
                    "Failed to process the uploaded files."
                });
            }
            return res.status(502).json({
                message: "Failed to communicate with AI service."
            });
        }
    }
);


// router.route("/uploads").post(
//     upload.fields([
//         {
//             name:"document_pdf",
//             maxCount:1
//         },
//         {
//             name:"Excel_Data_sheet",
//             maxCount:1
//         }
//     ]),async(req,res)=>{
//         console.log(req.files);
//         const pdf_filepath=req.files?.document_pdf[0]?.path
//         const excel_filepath=req.files?.Excel_Data_sheet[0]?.path
//         if (!pdf_filepath) {
//             return res.status(400).json({
//                 message: "PDF upload error"
//             });
//         }
//         if (!excel_filepath) {
//             return res.status(400).json({
//                 message: "excel sheet upload error"
//             });
//         }
//         console.log("PDF path being sent to FastAPI:", pdf_filepath);
//         console.log("Excel path being sent to FastAPI:", excel_filepath);
//         const response=await axios.post("http://127.0.0.1:8000/process",{
//             "document_pdf": pdf_filepath,
//             "excel_file":excel_filepath,
//         })
//         console.log("FastAPI response received:", response.data)

        
//         res.json({
//             workspace_id:response.data.workspace_id,
//             message:response.data.message,
//         })

//     }
// )

export default router






