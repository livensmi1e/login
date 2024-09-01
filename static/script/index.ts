import { AuthHandler } from "./auth.js"
import { OauthHandler } from "./oauth.js";
import { CreateUser, User } from "./type.js";
import { clearPasswordFields } from "./util.js";

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

const facebookButtons = document.querySelectorAll(".facebook-button button");
const googleButtons = document.querySelectorAll(".google-button button");
const githubButtons = document.querySelectorAll(".github-button button");

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
        const authHandler = new AuthHandler();
        const res = await authHandler.register(user);
        if (res.status_code === 201) {
            alert("Register successful");
            registerForm.style.display = 'none';
            loginForm.style.display = 'block';
        }
        else {
            alert("Register failed. Try again");
            clearPasswordFields();
        }
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
        const authHandler = new AuthHandler();
        const res = await authHandler.login(user);
        if (res.status_code == 200) {
            window.location.href = "/pages/dashboard.html"
        }
        else {
            alert("Login failed. Check your crendentials")
            window.location.reload()
        }
    } catch (error) {
        console.error(`Register error: ${error}`);
        window.location.href = "/pages/index.html"
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

googleButtons.forEach((button) => {
    button.addEventListener("click", async function (e) {
        e.preventDefault();
        try {
            const oauthHanler = new OauthHandler();
            const res = await oauthHanler.auth_url("google");
            if (res.status_code == 201 && "data" in res) {
                const auth_url = res.data.url;
                window.open(auth_url);
            }
        } catch (error) {
            console.error(`Oauth2 error: ${error}`);
        }
    })
});

facebookButtons.forEach((button) => {
    button.addEventListener("click", async function (e) {
        e.preventDefault();
        try {
            const oauthHanler = new OauthHandler();
            const res = await oauthHanler.auth_url("facebook");
            if (res.status_code == 201 && "data" in res) {
                const auth_url = res.data.url;
                window.open(auth_url);
            }
        } catch (error) {
            console.error(`Oauth2 error: ${error}`);
        }
    });
});

githubButtons.forEach((button) => {
    button.addEventListener("click", async function (e) {
        e.preventDefault();
        try {
            const oauthHanler = new OauthHandler();
            const res = await oauthHanler.auth_url("github");
            if (res.status_code == 201 && "data" in res) {
                const auth_url = res.data.url;
                window.open(auth_url);
            }
        } catch (error) {
            console.error(`Oauth2 error: ${error}`);
        }
    });
});