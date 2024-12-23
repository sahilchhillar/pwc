// LoginPage.js
import React from 'react';
import { Container, Box, TextField, Button, Typography, Link } from '@mui/material';
import './LoginPage.css';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const navigate = useNavigate();
  
  return (
    <Container maxWidth="sm" className="login-container">
      <Box className="login-box" p={4} boxShadow={3} borderRadius={2} textAlign="center">
        <Typography variant="h4" gutterBottom>Login</Typography>
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
              label="Password"
              variant="outlined"
              type="password"
              fullWidth
              required
            />
          </Box>
          <Button variant="contained" color="primary" fullWidth onClick={() => {
            navigate('/upload');
          }}>
            Submit
          </Button>
        </form>
        <Box mt={2}>
          <Link href="/forgot-password" underline="hover">
            Forgot Password?
          </Link>
        </Box>
        <Box mt={1}>
          <Typography variant="body2">
            Don’t have an account? <Link href="/register" underline="hover">Register here</Link>
          </Typography>
        </Box>
      </Box>
    </Container>
  );
}

export default LoginPage;
