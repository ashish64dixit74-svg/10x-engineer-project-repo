import { useEffect, useRef } from "react";
import Button from "./Button";

function Modal({ isOpen, title, children, onClose, footer }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    if (!isOpen) {
      return undefined;
    }

    const dialogElement = dialogRef.current;
    const previousActiveElement = document.activeElement;
    const focusableSelector =
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

    const focusableElements = dialogElement
      ? Array.from(dialogElement.querySelectorAll(focusableSelector))
      : [];

    if (focusableElements.length) {
      focusableElements[0].focus();
    } else if (dialogElement) {
      dialogElement.focus();
    }

    const onKeyDown = (event) => {
      if (event.key === "Escape") {
        onClose();
        return;
      }

      if (event.key !== "Tab" || !dialogElement) {
        return;
      }

      const modalFocusable = Array.from(dialogElement.querySelectorAll(focusableSelector));
      if (!modalFocusable.length) {
        event.preventDefault();
        return;
      }

      const firstElement = modalFocusable[0];
      const lastElement = modalFocusable[modalFocusable.length - 1];

      if (event.shiftKey && document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      } else if (!event.shiftKey && document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    };

    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      if (previousActiveElement && typeof previousActiveElement.focus === "function") {
        previousActiveElement.focus();
      }
    };
  }, [isOpen, onClose]);

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-backdrop" role="presentation" onClick={onClose}>
      <div
        ref={dialogRef}
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-label={title}
        tabIndex={-1}
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <h2>{title}</h2>
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>

        <div className="modal-body">{children}</div>

        {footer ? <div className="modal-footer">{footer}</div> : null}
      </div>
    </div>
  );
}

export default Modal;
