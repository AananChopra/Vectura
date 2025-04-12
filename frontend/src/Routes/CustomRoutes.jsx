import { Route, Routes } from "react-router-dom";
import Home from "../Components/Pages/Home";
import SignupPage from "../Components/Pages/SignupPage";
import LoginPage from "../Components/Pages/LoginPage";
import AiPage from "../Components/Pages/AiPage";


function CustomRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/SignUp" element={<SignupPage/>} />
            <Route path="/login" element={<LoginPage/>} />
            <Route path="/chat" element={<AiPage/>} />
        </Routes>
    );
};

export default CustomRoutes;