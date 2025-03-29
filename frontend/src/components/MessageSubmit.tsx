import React, { useState } from "react";
import "./MessageSubmit.css";

interface MessageFormData {
  title: string;
  content: string;
}

interface MessageSubmitProps {
  isOpen: boolean;
  onClose: () => void;
  location?: { lat: number; lng: number };
}

const MessageSubmit: React.FC<MessageSubmitProps> = ({
  isOpen,
  onClose,
  location,
}) => {
  const [formData, setFormData] = useState<MessageFormData>({
    title: "",
    content: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send the form data to your backend
    console.log("Form submitted:", formData);
    alert("Thank you for your submission! We will review it shortly.");
    setFormData({ title: "", content: "" });
    onClose();
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>
          ×
        </button>
        <div className="form-section">
          {location && (
            <div className="location-info">
              <h3>Selected Location</h3>
              <p>Latitude: {location.lat.toFixed(6)}</p>
              <p>Longitude: {location.lng.toFixed(6)}</p>
            </div>
          )}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="title">
                Got a rant about a pothole in Halifax?
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
                placeholder="Rant title"
              />
            </div>

            <div className="form-group">
              <label htmlFor="content">Message</label>
              <textarea
                id="content"
                name="content"
                value={formData.content}
                onChange={handleChange}
                required
                placeholder="Rant about your Halifax pothole"
                rows={6}
              />
            </div>

            <button type="submit" className="submit-btn">
              Submit Message
            </button>
          </form>
        </div>

        <div className="guidelines">
          <h2>Submission Guidelines</h2>
          <ul>
            <li>Keep your rant respectful</li>
            <li>Focus on your personal experiences</li>
            <li>Be specific about events you're discussing</li>
            <li>Proofread your message</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MessageSubmit;
