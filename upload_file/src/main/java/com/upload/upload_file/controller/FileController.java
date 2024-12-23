package com.upload.upload_file.controller;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import com.upload.upload_file.model.FileDocument;
import com.upload.upload_file.service.FileService;

@RestController
@RequestMapping("/api/v1/files")
public class FileController {
    @Autowired
    private FileService fileService;

    @PostMapping(value = "/upload", consumes = {MediaType.MULTIPART_FORM_DATA_VALUE}, 
                                    produces = {MediaType.APPLICATION_JSON_VALUE})
    public ResponseEntity<String> uploadFile(@RequestParam MultipartFile file) throws IOException{
        String fileId = fileService.uplodaFile(file);

        // String django_url = "http://127.0.0.1:8000/api/upload/";
        // RestTemplate restTemplate = new RestTemplate();

        // // Create headers
        // HttpHeaders headers = new HttpHeaders();
        // headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        // // Attach data 
        // MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        // body.add("file_id", fileId);

        // HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<MultiValueMap<String,Object>>(body, headers);

        // // Send request to Django
        // ResponseEntity<String> response = restTemplate.exchange(
        //     django_url,
        //     HttpMethod.GET,
        //     requestEntity, 
        //     String.class
        // );

        // String final_data = response.getBody();
        // System.out.println("Data: " + final_data);

        return ResponseEntity.ok("File uploaded successfully with ID: " + fileId);
    }

    @GetMapping("/{id}")
    public ResponseEntity<byte[]> getFile(@PathVariable String id) {
        FileDocument fileDocument = fileService.getFile(id);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + fileDocument.getFileName() + "\"")
                .contentType(MediaType.parseMediaType(fileDocument.getContentType()))
                .body(fileDocument.getData());
    }
}
