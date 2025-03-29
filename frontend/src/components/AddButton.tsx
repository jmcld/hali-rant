import styled from "styled-components";

const StyledAddButton = styled.button`
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 80px;
  height: 80px;
  font-size: 50px;
  border-radius: 50%;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  padding: 0;
  z-index: 1000;

  &:hover {
    background-color: #0056b3;
  }
`;

interface AddButtonProps {
  isActive: boolean;
  onClick: () => void;
}

const AddButton = ({ isActive, onClick }: AddButtonProps) => {
  return (
    <StyledAddButton onClick={onClick}>
      <span>{isActive ? "×" : "+"}</span>
    </StyledAddButton>
  );
};

export default AddButton;
