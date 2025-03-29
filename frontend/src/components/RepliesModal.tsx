import React, { useState } from "react";
import Modal from "./Modal";
import { Marker } from "../types";

interface RepliesModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedMarkerID: string | null;
  markers: Marker[];
  onAddReply?: (markerId: string, reply: string) => void;
}

const RepliesModal: React.FC<RepliesModalProps> = ({
  isOpen,
  onClose,
  selectedMarkerID,
  markers,
  onAddReply,
}) => {
  const [newReply, setNewReply] = useState("");

  const selectedMarker = markers.find((m) => m.id === selectedMarkerID) || null;

  if (!selectedMarker) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (newReply.trim() && onAddReply) {
      onAddReply(selectedMarker.id, newReply.trim());
      setNewReply("");
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={selectedMarker.title}>
      <div>
        <p>{selectedMarker.body}</p>
        <h3>Replies</h3>
        {selectedMarker.replies && selectedMarker.replies.length > 0 ? (
          selectedMarker.replies.map((reply, index) => (
            <div
              key={index}
              style={{
                marginTop: "10px",
                padding: "10px",
                borderBottom: "1px solid #eee",
              }}
            >
              <p>{reply}</p>
            </div>
          ))
        ) : (
          <p>No replies yet. Be the first to reply!</p>
        )}

        <form onSubmit={handleSubmit} style={{ marginTop: "20px" }}>
          <textarea
            value={newReply}
            onChange={(e) => setNewReply(e.target.value)}
            placeholder="Write your reply..."
            style={{
              width: "100%",
              minHeight: "100px",
              padding: "10px",
              marginBottom: "10px",
              borderRadius: "4px",
              border: "1px solid #ddd",
              backgroundColor: "white",
              color: "black",
            }}
          />
          <button
            type="submit"
            style={{
              padding: "8px 16px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Submit Reply
          </button>
        </form>
      </div>
    </Modal>
  );
};

export default RepliesModal;
