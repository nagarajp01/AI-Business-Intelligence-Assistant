import express from"express"
import axios from "axios"
const router=express.Router()


router.route("/ask").post(
    async(req,res)=>{
        try {
            const response=await axios.post("http://127.0.0.1:8000/ask",{
                question:req.body.question,
                workspace_id: req.body.workspace_id
            });
            res.json(response.data);

        } catch (error) {
            console.error(error.message);
            res.status(500).json({
                message: "Failed to communicate with AI service"
            });
            
        }
    }
);

export default router;




