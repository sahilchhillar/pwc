// FileUploadPage.js
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Container, Box, Typography, Button, IconButton } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DeleteIcon from '@mui/icons-material/Delete';
import './FileUploadPage.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function FileUploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      alert("Only PDF and DOC files are allowed!");
      return;
    }
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    accept: {
      "application/pdf": [".pdf"],
      "application/msword": [".doc", ".docx"],
    },
  });

  const handleManualUpload = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && (selectedFile.type === "application/pdf" || selectedFile.type === "application/msword")) {
      setFile(selectedFile);
    } else {
      alert("Only PDF and DOC files are allowed!");
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8080/api/v1/files/upload", formData, {
          headers: {
            "Content-type": "multipart/form-data",
          },
        }
      );
      if(response.status === 200){
        setMessage("File uploaded successfully");
        console.log(message);
      }else{
        setMessage("Failed to upload the file");
      }
    } catch (error) {
      console.error("Error uploading file: ", error);
      setMessage("Error uploading the file. Please try again.");
    }
  }

  return (
    <Container maxWidth="sm" className="file-upload-container">
      <Box className="file-upload-box" p={4} boxShadow={3} borderRadius={2} textAlign="center">
        <Typography variant="h4" gutterBottom>
          Upload File
        </Typography>
        <Box
          {...getRootProps()}
          className={`dropzone ${isDragActive ? 'active' : ''}`}
          mb={2}
        >
          <input {...getInputProps()} />
          <UploadFileIcon sx={{ fontSize: 50, color: '#1976d2' }} />
          <Typography variant="body1">
            {isDragActive ? "Drop the file here..." : "Drag and drop your PDF or DOC file here, or click to select a file"}
          </Typography>
        </Box>
        <Button
          variant="contained"
          component="label"
          color="primary"
          fullWidth
          sx={{ mb: 2 }}
        >
          Choose File
          <input
            type="file"
            hidden
            accept=".pdf, .doc, .docx"
            onChange={handleManualUpload}
          />
        </Button>
        <Button
            variant="contained"
            color="success"
            fullWidth
            sx={{ mt: 2 }}
            onClick={() => {
                if (!file) {
                  alert("Please upload a file before submitting!");
                } else {
                  handleSubmit();
                  navigate("/success");
                }
            }}
            >
            Submit
        </Button>
        {file && (
          <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="body2">
              Selected File: {file.name}
            </Typography>
            <IconButton color="secondary" onClick={handleRemoveFile}>
              <DeleteIcon />
            </IconButton>
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default FileUploadPage;
