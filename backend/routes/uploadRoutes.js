
import { Router } from "express";
import { upload } from "../middleware/multer.middleware.js";
import axios from "axios";
import path from "node:path";

const router = Router();

// Python FastAPI URL
const PYTHON_API_URL = (
    process.env.PYTHON_API_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

router.route("/uploads").post(

    // Multer file upload middleware
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

    // Process uploaded files
    async (req, res) => {

        try {

            const pdfFile = req.files?.document_pdf?.[0];
            const excelFile = req.files?.Excel_Data_sheet?.[0];

            // Check whether at least one file is uploaded
            if (!pdfFile && !excelFile) {
                return res.status(400).json({
                    message: "Please upload at least one file (PDF or Excel)."
                });
            }

            // Validate PDF extension
            if (
                pdfFile &&
                path.extname(pdfFile.originalname).toLowerCase() !== ".pdf"
            ) {
                return res.status(400).json({
                    message: "The document must be a PDF file."
                });
            }

            // Validate Excel/CSV extension
            if (
                excelFile &&
                ![".xlsx", ".csv"].includes(
                    path.extname(excelFile.originalname).toLowerCase()
                )
            ) {
                return res.status(400).json({
                    message: "The data sheet must be an Excel (.xlsx) or CSV file."
                });
            }

            // Create multipart FormData
            const formData = new FormData();

            // Attach PDF file
            if (pdfFile) {
                formData.append(
                    "document_pdf",
                    new Blob(
                        [pdfFile.buffer],
                        { type: pdfFile.mimetype }
                    ),
                    pdfFile.originalname
                );
            }

            // Attach Excel/CSV file
            if (excelFile) {
                formData.append(
                    "excel_file",
                    new Blob(
                        [excelFile.buffer],
                        { type: excelFile.mimetype }
                    ),
                    excelFile.originalname
                );
            }

            // Forward actual files to Python FastAPI
            const response = await axios.post(
                `${PYTHON_API_URL}/process`,
                formData,
                {
                    timeout: 600000
                }
            );

            // Return workspace details
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

            if (
                error.code === "ECONNABORTED" ||
                error.code === "ETIMEDOUT"
            ) {
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

export default router;



