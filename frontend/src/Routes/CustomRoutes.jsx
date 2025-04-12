import { Route, Routes } from "react-router-dom";
import Home from "../Components/Pages/Home";
import SignupPage from "../Components/Pages/SignupPage";
import LoginPage from "../Components/Pages/LoginPage";


function CustomRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/SignUp" element={<SignupPage/>} />
            <Route path="/login" element={<LoginPage/>} />
        </Routes>
    );
};

export default CustomRoutes;