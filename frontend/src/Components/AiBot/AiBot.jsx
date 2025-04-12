import { useState, useEffect, useRef } from "react";
import { Send, Bot } from "lucide-react";
import "./AiBot.css"; // CSS file for styling

const AiBot = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userResponses, setUserResponses] = useState({});
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ sender: "bot", text: "Hello! Let's get started. 😃" }]);
    }
  }, [messages]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleUserInput = () => {
    if (!userInput.trim()) return;

    const updatedMessages = [
      ...messages,
      { sender: "user", text: userInput },
    ];
    setMessages(updatedMessages);

    setUserResponses((prev) => ({
      ...prev,
      [currentQuestionIndex]: userInput,
    }));

    setUserInput("");

    setTimeout(() => {
      // Add the bot's question after the user submits their answer
      const nextQuestion = questions[currentQuestionIndex + 1];
      if (nextQuestion) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: "bot", text: nextQuestion },
        ]);
      }

      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }, 500);
  };

  const questions = [
    "👋 Hi there! I’m here to help you manage your debts. Ready?",
    "1️⃣ What’s your full name?",
    "2️⃣ How old are you?",
    "3️⃣ Where do you live?",
    "4️⃣ What currency do you use?",
    "5️⃣ What is your monthly income?",
    "6️⃣ What’s your total monthly expenses?",
    "7️⃣ How many loans do you currently have?",
    "8️⃣ Do you miss payments frequently?",
    "9️⃣ On a scale of 1 to 5, how do you feel about your debt situation?",
    "🔚 That’s all! Now, I’ll generate a report based on your responses.",
  ];

  return (
    <div className="ai-chat-container">
      <div className="chat-header">
        <Bot size={24} />
        <span>Ventura Debt Assistant</span>
      </div>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender === "bot" ? "bot" : "user"}`}
          >
            <Bot size={24} className="message-bot-logo" />
            {message.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {currentQuestionIndex >= questions.length ? (
        <div className="chat-footer">
          <button className="submit-btn">Generate Report</button>
        </div>
      ) : (
        <div className="chat-footer">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder={questions[currentQuestionIndex]}
            className="chat-input"
          />
          <button className="send-btn" onClick={handleUserInput}>
            <Send size={18} />
          </button>
        </div>
      )}
    </div>
  );
};

export default AiBot;
