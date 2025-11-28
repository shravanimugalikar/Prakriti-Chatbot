document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("consultationForm");
    const successMessage = document.getElementById("successMessage");

    function clearErrors() {
        document.querySelectorAll(".error").forEach((el) => el.remove());
        form.querySelectorAll("input, textarea").forEach((el) => {
            el.style.border = "";
            el.removeAttribute("aria-invalid");
        });
    }

    function showError(field, message) {
        const error = document.createElement("div");
        error.className = "error";
        error.textContent = message;
        field.style.border = "1.5px solid #e53935";
        field.setAttribute("aria-invalid", "true");
        field.parentNode.appendChild(error);
    }

    // ---------------------------
    // VALIDATION LOGIC
    // ---------------------------
    function validateForm() {
        clearErrors();
        let valid = true;

        const nameEl = document.getElementById("name");
        const emailEl = document.getElementById("email");
        const phoneEl = document.getElementById("phone");
        const dateEl = document.getElementById("date");
        const msgEl = document.getElementById("message");

        const name = nameEl.value.trim();
        const email = emailEl.value.trim();
        const phone = phoneEl.value.trim();
        const date = dateEl.value;
        const msg = msgEl.value.trim();

        // Name
        if (!name || name.length < 3) {
            showError(nameEl, "Please enter a valid full name");
            valid = false;
        }

        // Email
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) {
            showError(emailEl, "Email is required");
            valid = false;
        } else if (!emailPattern.test(email)) {
            showError(emailEl, "Please enter a valid email address");
            valid = false;
        }

        // Phone
        const phoneDigits = phone.replace(/\D/g, "");
        if (!phone) {
            showError(phoneEl, "Phone number is required");
            valid = false;
        } else if (!/^\d{10}$/.test(phoneDigits)) {
            showError(phoneEl, "Enter a valid 10-digit phone number");
            valid = false;
        }

        // Date
        if (!date) {
            showError(dateEl, "Please select a date");
            valid = false;
        } else {
            const today = new Date();
            const selected = new Date(date);
            today.setHours(0, 0, 0, 0);
            selected.setHours(0, 0, 0, 0);
            if (selected < today) {
                showError(dateEl, "Date cannot be in the past");
                valid = false;
            }
        }

        // Message
        if (!msg) {
            showError(msgEl, "Please describe your concern");
            valid = false;
        }

        return valid;
    }

    // ---------------------------
    // FORM SUBMISSION HANDLER
    // ---------------------------
    form.addEventListener("submit", function (e) {

        successMessage.style.display = "none";

        if (!validateForm()) {
            e.preventDefault(); // Stop form from submitting
            return;
        }

        // Allow submission to submit.php
        successMessage.textContent = "Submitting... Please wait.";
        successMessage.style.display = "block";
        successMessage.style.color = "green";
    });

});
