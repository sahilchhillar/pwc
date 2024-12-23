package com.upload.upload_file;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable()) // Disable CSRF protection for APIs
                .authorizeHttpRequests(requests -> requests
                        .anyRequest().permitAll()); // Allow all requests (adjust as needed for your use case)
        
        return http.build();
    }
}
