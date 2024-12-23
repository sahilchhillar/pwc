// RegisterPage.js
import React from 'react';
import { Container, Box, TextField, Button, Typography, Link } from '@mui/material';
import './RegisterPage.css';

function RegisterPage() {
  return (
    <Container maxWidth="sm" className="register-container">
      <Box className="register-box" p={4} boxShadow={3} borderRadius={2} textAlign="center">
        <Typography variant="h4" gutterBottom>Register</Typography>
        <form>
          <Box mb={3}>
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              required
            />
          </Box>
          <Box mb={3}>
            <TextField
              label="Email"
              variant="outlined"
              type="email"
              fullWidth
              required
            />
          </Box>
          <Box mb={3}>
            <TextField
              label="Password"
              variant="outlined"
              type="password"
              fullWidth
              required
            />
          </Box>
          <Box mb={3}>
            <TextField
              label="Confirm Password"
              variant="outlined"
              type="password"
              fullWidth
              required
            />
          </Box>
          <Button variant="contained" color="primary" fullWidth>
            Register
          </Button>
        </form>
        <Box mt={2}>
          <Typography variant="body2">
            Already have an account? <Link href="/login" underline="hover">Login here</Link>
          </Typography>
        </Box>
      </Box>
    </Container>
  );
}

export default RegisterPage;
