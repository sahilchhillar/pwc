package com.upload.upload_file.service;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.upload.upload_file.model.FileDocument;
import com.upload.upload_file.repository.FileRepository;

@Service
public class FileService {
    @Autowired
    private FileRepository fileRepository;

    public String uplodaFile(MultipartFile file) throws IOException {
        FileDocument fileDocument = new FileDocument();
        fileDocument.setFileName(file.getOriginalFilename());
        fileDocument.setContentType(file.getContentType());
        fileDocument.setData(file.getBytes());

        fileDocument = fileRepository.save(fileDocument);
        return fileDocument.getId();
    }

    public FileDocument getFile(String id){
        return fileRepository.findById(id).orElseThrow(() -> new RuntimeException("file not found"));
    }
}
