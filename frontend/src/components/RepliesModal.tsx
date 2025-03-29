import React from "react";
import Modal from "./Modal";
import { Marker } from "../types";

interface RepliesModalProps {
  isOpen: boolean;
  onClose: () => void;
  marker: Marker | null;
}

const RepliesModal: React.FC<RepliesModalProps> = ({
  isOpen,
  onClose,
  marker,
}) => {
  if (!marker) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={marker.title}>
      <div>
        <p>{marker.body}</p>
        <h3>Replies</h3>
        {marker.replies && marker.replies.length > 0 ? (
          marker.replies.map((reply, index) => (
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
      </div>
    </Modal>
  );
};

export default RepliesModal;
