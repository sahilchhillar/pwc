package com.upload.upload_file.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.upload.upload_file.model.FileDocument;

@Repository
public interface FileRepository extends MongoRepository<FileDocument, String> {
    
}
