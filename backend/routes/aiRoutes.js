import express from"express"
import axios from "axios"
const router=express.Router()


router.route("/ask").post(
    async(req,res)=>{
        try {
            const response=await axios.post("http://127.0.0.1:8000/ask",{
                question:req.body.question,
                workspace_id: req.body.workspace_id
            },
            {
                timeout:600000,
                responseType:"stream"
            }
        );
        // return res.json(response.data);
        res.setHeader(
            "Content-Type",
            response.headers["content-type"] || "text/plain"
        );
        res.status(response.status);
        response.data.pipe(res);
    } catch (error) {
        console.error("AI question processing failed:",error.response?.data || error.message);
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
                    "Failed to process your question."
            });
        }
        res.status(502).json({
            message: "Failed to communicate with AI service"
        });
            
        }
    }
);

router.get("/download-report/:workspaceId", async (req, res) => {
    try {
        const response = await axios.get(
            `http://127.0.0.1:8000/download-report/${req.params.workspaceId}`,
            {
                responseType: "stream",
                timeout: 600000
            }
        );

        res.setHeader(
            "Content-Type",
            "application/pdf"
        );

        res.setHeader(
            "Content-Disposition",
            'attachment; filename="BusinessFileReport.pdf"'
        );

        response.data.pipe(res);

    } catch (error) {
        console.error("PDF download failed:", error.message);

        if (error.response) {
            return res.status(error.response.status).json({
                message: "Failed to download PDF report."
            });
        }

        return res.status(502).json({
            message: "Unable to communicate with AI service."
        });
    }
});

export default router;




