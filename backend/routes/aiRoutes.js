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
                timeout:600000
            }
        );
        return res.json(response.data);
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

export default router;




