import { Route, Routes } from "react-router-dom";
import Home from "../Components/Pages/Home";
import SignupPage from "../Components/Pages/SignupPage";


function CustomRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/SignUp" element={<SignupPage/>} />
        </Routes>
    );
};

export default CustomRoutes;