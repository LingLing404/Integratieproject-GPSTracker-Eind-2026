const form = document.querySelector("#login-form");
const message = document.querySelector("#form-message");
const params = new URLSearchParams(window.location.search);

if (params.get("error")) {
    message.textContent = "Login mislukt. Controleer je e-mailadres en wachtwoord.";
}
