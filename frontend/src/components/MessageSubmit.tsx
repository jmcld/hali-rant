import React, { useState } from 'react';
import './MessageSubmit.css';

interface MessageFormData {
    title: string;
    content: string;
    email: string;
}

interface MessageSubmitProps {
    isOpen: boolean;
    onClose: () => void;
}

const MessageSubmit: React.FC<MessageSubmitProps> = ({ isOpen, onClose }) => {
    const [formData, setFormData] = useState<MessageFormData>({
        title: '',
        content: '',
        email: ''
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Here you would typically send the form data to your backend
        console.log('Form submitted:', formData);
        alert('Thank you for your submission! We will review it shortly.');
        setFormData({ title: '', content: '', email: '' });
        onClose();
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <button className="close-button" onClick={onClose}>×</button>
                <div className="form-section">
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="title">Got a rant about a pothole in Halifax?</label>
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
                        <li>Keep your message respectful and constructive</li>
                        <li>Focus on your personal experiences and observations</li>
                        <li>Be specific about locations or events you're discussing</li>
                        <li>Proofread your message before submitting</li>
                        <li>Ensure your content is original and authentic</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default MessageSubmit; 