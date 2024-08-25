import { AuthHandler } from "./auth"
import { CreateUser } from "./type";

const passwordElement = document.querySelector(".register-pass") as HTMLInputElement;
const confirmPasswordElement = document.querySelector(".register-confirm-pass") as HTMLInputElement;
const registerEmailElement = document.querySelector(".register-email") as HTMLInputElement;
const registerFormElement = document.querySelector("register-form") as HTMLFormElement;

const password = passwordElement ? passwordElement.value : "";
const confirmPassword = confirmPasswordElement ? confirmPasswordElement.value : "";
const registerEmail = registerEmailElement ? registerEmailElement.value : "";



export function getPasswordFields(): { password: string, confirmPassword: string } {
    return { password, confirmPassword };
}

export function clearPasswordFields(): void {
    if (passwordElement) passwordElement.value = "";
    if (confirmPasswordElement) confirmPasswordElement.value = "";
}

const authHandler = new AuthHandler();

registerFormElement.addEventListener("submit", async function (e) {
    e.preventDefault();
    console.log(registerEmail);
    const user: CreateUser = {
        email: registerEmail,
        password: password,
        comfirmPasword: confirmPassword
    }
    await authHandler.register(user);
});