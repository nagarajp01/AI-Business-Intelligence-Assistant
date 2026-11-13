import multer from "multer";

const storage = multer.memoryStorage();

export const upload = multer({
    storage,
    limits: {
        fileSize: 20 * 1024 * 1024
    },
    fileFilter: (req, file, cb) => {
        const allowedTypes = {
            document_pdf: [
                "application/pdf"
            ],
            Excel_Data_sheet: [
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/vnd.ms-excel",
                "text/csv",
                "application/csv"
            ]
        };

        const allowed = allowedTypes[file.fieldname];

        if (!allowed || !allowed.includes(file.mimetype)) {
            return cb(
                new Error(`Invalid file type for ${file.fieldname}`)
            );
        }

        cb(null, true);
    }
});



