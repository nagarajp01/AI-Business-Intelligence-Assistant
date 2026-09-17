import { Router } from "express";
import { upload } from "../middleware/multer.middleware.js";

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
    ]),(req,res)=>{
        console.log(req.files);
        res.json({
            message:"Files Uploaded Successfully",
            files:req.files
        })

    }
)

export default router