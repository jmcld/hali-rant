import React, { useState } from "react";
import "./MessageSubmit.css";
import { url } from "../config";
import Modal from "./Modal";

interface MessageFormData {
  title: string;
  content: string;
  category: string;
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
    category: "pothole", // Default category
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (!location) {
        alert("Please select a location on the map first!");
        return;
      }

      const response = await fetch(`${url}/rants/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: formData.title,
          body: formData.content,
          location: {
            lat: location.lat,
            lon: location.lng,
          },
          categ: formData.category,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit rant");
      }

      const result = await response.json();
      console.log("Rant submitted successfully:", result);
      alert("Thank you for your submission! We will review it shortly.");
      setFormData({ title: "", content: "", category: "pothole" });
      onClose();
    } catch (error) {
      console.error("Error submitting rant:", error);
      alert("Failed to submit your rant. Please try again later.");
    }
  };

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Submit Your Rant">
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

          <div className="form-group">
            <label htmlFor="category">Category</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="pothole">Pothole</option>
              <option value="positive">Positive</option>
              <option value="other">Other</option>
            </select>
          </div>

          <button type="submit" className="submit-btn">
            Submit Message
          </button>
        </form>
      </div>

      <div className="location-info">
        <h3>Submission Guidelines</h3>
        <p>
          Keep your rant respectful and constructive. Focus on sharing your
          personal experiences and observations.
        </p>
        <p>
          Be specific about the events or situations you're discussing. This
          helps others understand your perspective better.
        </p>
        <p>
          Take a moment to proofread your message before submitting to ensure
          clarity and professionalism.
        </p>
      </div>
    </Modal>
  );
};

export default MessageSubmit;
