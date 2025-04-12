import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "./Signup.css";

const Signup = () => {
  const [formData, setFormData] = useState({
    name: "", // Keep 'name' as per backend
    email: "",
    password: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const data = {
      name: formData.name,
      email: formData.email,
      password: formData.password,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Registration failed");
      }

      setFormData({ name: "", email: "", password: "" });
      navigate("/login"); // Redirect user to login page after successful registration
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <motion.form
        className="register-form"
        onSubmit={handleSubmit}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h2>Register</h2>

        {error && <p className="error-message">{error}</p>}

        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email Address"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <motion.button
          type="submit"
          className="btn-primary"
          whileHover={{ scale: 1.05 }}
          disabled={loading}
        >
          {loading ? "Registering..." : "Register"}
        </motion.button>
        <motion.button
          className="btn-outline"
          whileHover={{ scale: 1.05 }}
          onClick={() => navigate("/login")}
          type="button"
        >
          Back to Login
        </motion.button>
      </motion.form>
    </div>
  );
};

export default Signup;