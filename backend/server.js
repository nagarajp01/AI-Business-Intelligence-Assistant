import express from "express"
console.log("1. Starting server.js");
import aiRoutes from "./routes/aiRoutes.js";
console.log("2. aiRoutes imported");
import uploadRoutes from "./routes/uploadRoutes.js"
console.log("3. uploadRoutes imported");
// const express=require("express");

const app=express();
console.log("4. Express app created");
const PORT=5000;
app.use(express.json());
console.log("5. JSON middleware added");
app.use("/api",aiRoutes)
console.log("6. AI routes added");
app.use("/api",uploadRoutes)
console.log("7. Upload routes added");
app.get("/",(req,res)=>{
    res.json({
        message:"Express backend is running"
    })
})


app.listen(PORT,()=>{
    console.log(`Express server running on http://localhost:${PORT}`)
})

