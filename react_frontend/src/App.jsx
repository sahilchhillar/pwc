import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './login/LoginPage';
import RegisterPage from './register/RegisterPage';
import FileUploadPage from './dragndrop/FileUploadPage';
import SuccessPage from './success/SuccessPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/upload" element={<FileUploadPage />} />
        <Route path="/success" element={<SuccessPage />} />
        <Route path="/" element={<FileUploadPage />} />
      </Routes>
    </Router> 
  );
}

export default App;
