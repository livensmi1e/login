import { AuthHandler } from "./auth.js"
import { CreateUser, User } from "./type.js";

const passwordElement = document.getElementById("register-pass") as HTMLInputElement;
const confirmPasswordElement = document.getElementById("register-confirm-pass") as HTMLInputElement;
const registerEmailElement = document.getElementById("register-email") as HTMLInputElement;
const registerFormElement = document.querySelector(".register-form") as HTMLFormElement;

const loginPassElement = document.getElementById("login-pass") as HTMLInputElement;
const loginEmailElement = document.getElementById("login-email") as HTMLInputElement;
const loginFormElement = document.querySelector(".login-form") as HTMLInputElement;

const registerLink = document.querySelector(".register-link a") as HTMLAnchorElement;
const loginLink = document.querySelector(".login-link a") as HTMLAnchorElement;

const loginForm = document.querySelector(".login-form") as HTMLDivElement;
const registerForm = document.querySelector(".register-form") as HTMLDivElement;

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
    try {
        const res = await authHandler.register(user);
    } catch (error) {
        console.error(`Login error: ${error}`);
    }
});

loginFormElement.addEventListener("submit", async function (e) {
    e.preventDefault();
    const password = loginPassElement ? loginPassElement.value : "";
    const email = loginEmailElement ? loginEmailElement.value : "";
    const user: User = { email, password };
    try {
        const res = await authHandler.login(user);
    } catch (error) {
        console.error(`Register error: ${error}`);
    }
});


registerLink.addEventListener("click", function () {
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
});

loginLink.addEventListener("click", function () {
    registerForm.style.display = 'none';
    loginForm.style.display = 'block';
});
