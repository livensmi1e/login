import { AuthHandler } from "./auth.js"
import { CreateUser } from "./type.js";

const passwordElement = document.getElementById("register-pass") as HTMLInputElement;
const confirmPasswordElement = document.getElementById("register-confirm-pass") as HTMLInputElement;
const registerEmailElement = document.getElementById("register-email") as HTMLInputElement;
const registerFormElement = document.querySelector(".register-form") as HTMLFormElement;

export function clearPasswordFields(): void {
    if (passwordElement) passwordElement.value = "";
    if (confirmPasswordElement) confirmPasswordElement.value = "";
}

const authHandler = new AuthHandler();

registerFormElement.addEventListener("submit", async function (e) {
    e.preventDefault();
    const password = passwordElement ? passwordElement.value : "";
    const confirmPassword = confirmPasswordElement ? confirmPasswordElement.value : "";
    const registerEmail = registerEmailElement ? registerEmailElement.value : "";
    const user: CreateUser = {
        email: registerEmail,
        password: password,
        comfirmPasword: confirmPassword
    }
    const res = await authHandler.register(user);
});