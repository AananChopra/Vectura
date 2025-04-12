import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "./login.css";

// 🔐 Function to get CSRF token from cookies
const getCookie = (name) => {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="))
    ?.split("=")[1];
  return cookieValue || "";
};

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // 🧠 Handle input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 🚀 Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const { email, password } = formData;

    if (!email || !password) {
      setError("⚠ All fields are required!");
      setLoading(false);
      return;
    }

    try {
      const csrfToken = getCookie("csrftoken");

      const response = await fetch("http://localhost:8000/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        // 🧾 Save token and user details
        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));

        // 🧭 Navigate to home
        navigate("/");
        window.location.reload();
      } else {
        setError(data.error || "❌ Invalid credentials");
      }
    } catch (err) {
      setError("❌ Something went wrong. Try again!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="login-container"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <motion.form
        onSubmit={handleSubmit}
        className="login-form"
        initial={{ opacity: 0, scale: 0.9 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5, ease: "easeInOut" }}
      >
        <h2>Login to Vectura</h2>

        {error && <p className="login-error">{error}</p>}

        <motion.input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
          whileFocus={{ scale: 1.05, borderColor: "#50BFA5" }}
        />

        <motion.input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
          whileFocus={{ scale: 1.05, borderColor: "#50BFA5" }}
        />

        <motion.button
          type="submit"
          className="login-btn-primary"
          disabled={loading}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {loading ? "Logging in..." : "Login"}
        </motion.button>
      </motion.form>
    </motion.div>
  );
};

export default Login;