import express from "express"
import aiRoutes from "./routes/aiRoutes.js";
import uploadRoutes from "./routes/uploadRoutes.js"

// const express=require("express");

const app=express();

const PORT=5000;
app.use(express.json());

app.use("/api",aiRoutes)
app.use("/api",uploadRoutes)

app.get("/",(req,res)=>{
    res.json({
        message:"Express backend is running"
    })
})


app.listen(PORT,()=>{
    console.log(`Express server running on http://localhost:${PORT}`)
})

