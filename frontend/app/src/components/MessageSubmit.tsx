import React, { useState } from 'react';

interface MessageFormData {
    title: string;
    content: string;
    email: string;
}

const MessageSubmit: React.FC = () => {
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
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    return (
        <div className="message-submit-container">
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

            <style jsx>{`
                .message-submit-container {
                    max-width: 800px;
                    margin: 2rem auto;
                    padding: 0 2rem;
                }

                .form-section {
                    background: white;
                    padding: 2rem;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }

                .form-group {
                    margin-bottom: 1.5rem;
                }

                label {
                    display: block;
                    margin-bottom: 0.5rem;
                    font-weight: 500;
                    color: #333;
                }

                input[type="text"],
                input[type="email"],
                textarea {
                    width: 100%;
                    padding: 0.75rem;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 1rem;
                    transition: border-color 0.3s ease;
                }

                input[type="text"]:focus,
                input[type="email"]:focus,
                textarea:focus {
                    outline: none;
                    border-color: #007bff;
                }

                textarea {
                    resize: vertical;
                }

                .submit-btn {
                    background: linear-gradient(135deg, #007bff, #00bcd4);
                    color: white;
                    border: none;
                    padding: 1rem 2rem;
                    border-radius: 4px;
                    font-size: 1rem;
                    cursor: pointer;
                    transition: transform 0.2s ease;
                }

                .submit-btn:hover {
                    transform: translateY(-2px);
                }

                .guidelines {
                    margin-top: 2rem;
                    padding: 1.5rem;
                    background: #f8f9fa;
                    border-radius: 4px;
                }

                .guidelines h2 {
                    color: #007bff;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                }

                .guidelines ul {
                    list-style-position: inside;
                }

                .guidelines li {
                    margin-bottom: 0.5rem;
                }
            `}</style>
        </div>
    );
};

export default MessageSubmit; 