import { AuthHandler } from "./auth.js";

const logoutButton = document.querySelector(".button button") as HTMLButtonElement;

logoutButton.addEventListener("click", async function (e) {
    e.preventDefault();
    try {
        const authHander = new AuthHandler();
        authHander.logout();
        window.location.href = "/pages/index.html"
    } catch (error) {
        alert(`Logout error: ${error}`);
    }
});