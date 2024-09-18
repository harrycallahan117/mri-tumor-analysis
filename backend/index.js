const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();

// Configure Multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({
    storage,
    limits: { fileSize: 100 * 1024 * 1024 } // 10 MB limit
  });

// Create an upload directory if it doesn't exist
const fs = require('fs');
const uploadDir = 'uploads/';
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

// Handle the file upload
app.post('/upload', upload.single('mri'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded');
  }
  // Process image here
  res.send('MRI Uploaded Successfully');
});

// Cleanup endpoint to delete old files
app.post('/cleanup', (req, res) => {
    const expiryTime = 1 * 60 * 60 * 1000; // 1 hour
    fs.readdir(uploadDir, (err, files) => {
      if (err) return res.status(500).send('Error reading files');
  
      const now = Date.now();
      files.forEach((file) => {
        const filePath = path.join(uploadDir, file);
        fs.stat(filePath, (err, stats) => {
          if (err) return console.error(err);
  
          // If file is older than 24 hours, delete it
          if (now - stats.mtimeMs > expiryTime) {
            fs.unlink(filePath, (err) => {
              if (err) return console.error(err);
              console.log(`Deleted old file: ${file}`);
            });
          }
        });
      });
    });
    res.send('Cleanup process initiated');
  });  

// Start the server
app.listen(4000, () => console.log('Server running on port 4000'));