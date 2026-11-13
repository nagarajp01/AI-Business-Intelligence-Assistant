import express from "express";
import cors from "cors";

import aiRoutes from "./routes/aiRoutes.js";

import uploadRoutes from "./routes/uploadRoutes.js";


const app = express();


// CORS configuration
app.use(cors({
    origin: [
        "http://localhost:5173",
        process.env.FRONTEND_URL
    ].filter(Boolean)
}));

// Render port
const PORT = process.env.PORT || 5000;

app.use(express.json());


// API routes
app.use("/api", aiRoutes);


app.use("/api", uploadRoutes);


// Health check
app.get("/", (req, res) => {
    res.json({
        message: "Express backend is running"
    });
});

// Handle unknown routes
app.use((req, res) => {
    res.status(404).json({
        message: "Route not found"
    });
});

// Handle unexpected server errors
app.use((err, req, res, next) => {
    console.error("Express server error:", err.message);

    if (res.headersSent) {
        return next(err);
    }

    res.status(500).json({
        message: "Internal server error"
    });
});

// Start server
app.listen(PORT, "0.0.0.0", () => {
    console.log(`Express server running on port ${PORT}`);
});



