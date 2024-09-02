import { AuthHandler } from "./auth.js"
import { OauthHandler } from "./oauth.js";
import { CreateUser, User, RecoverRequest, PasswordReset } from "./type.js";
import { clearPasswordFields } from "./util.js";

const passwordElement = document.getElementById("register-pass") as HTMLInputElement;
const confirmPasswordElement = document.getElementById("register-confirm-pass") as HTMLInputElement;
const registerEmailElement = document.getElementById("register-email") as HTMLInputElement;
const registerFormElement = document.querySelector(".register-form form") as HTMLFormElement;

const loginPassElement = document.getElementById("login-pass") as HTMLInputElement;
const loginEmailElement = document.getElementById("login-email") as HTMLInputElement;
const loginFormElement = document.querySelector(".login-form form") as HTMLFormElement;

const registerLink = document.querySelector(".register-link a") as HTMLAnchorElement;
const loginLink = document.querySelector(".login-link a") as HTMLAnchorElement;

const loginForm = document.querySelector(".login-form") as HTMLDivElement;
const registerForm = document.querySelector(".register-form") as HTMLDivElement;

const facebookButtons = document.querySelectorAll(".facebook-button button");
const googleButtons = document.querySelectorAll(".google-button button");
const githubButtons = document.querySelectorAll(".github-button button");

const dashboardElement = document.querySelector(".dashboard") as HTMLDivElement;
const resetEmailElement = document.getElementById("reset-email") as HTMLInputElement;
const logoutButton = document.querySelector(".logout button") as HTMLButtonElement;
const resetButton = document.querySelector(".reset button") as HTMLInputElement;

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
        console.error(`Register error: ${error}`);
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
            loginForm.style.display = 'none';
            dashboardElement.style.display = 'flex';
        }
        else {
            alert("Login failed. Check your crendentials")
            window.location.reload()
        }
    } catch (error) {
        console.error(`Login error: ${error}`);
        window.location.reload();
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
                window.addEventListener("message", (e) => {
                    if (e.origin == window.location.origin) {
                        loginForm.style.display = 'none';
                        dashboardElement.style.display = 'flex';
                    }
                });
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
                window.addEventListener("message", (e) => {
                    if (e.origin == window.location.origin) {
                        loginForm.style.display = 'none';
                        dashboardElement.style.display = 'flex';
                    }
                });
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
                window.addEventListener("message", (e) => {
                    if (e.origin == window.location.origin) {
                        loginForm.style.display = 'none';
                        dashboardElement.style.display = 'flex';
                    }
                });
            }
        } catch (error) {
            console.error(`Oauth2 error: ${error}`);
        }
    });
});

logoutButton.addEventListener("click", async function (e) {
    e.preventDefault();
    try {
        const authHander = new AuthHandler();
        const res = await authHander.logout();
        if (res.status_code == 200) {
            window.location.reload();
        }
    } catch (error) {
        alert(`Logout error: ${error}`);
    }
});

resetButton.addEventListener("click", async function (e) {
    const email = resetEmailElement.value;
    if (email == "") {
        alert("Please provide your email");
    }
    else {
        const authHander = new AuthHandler();
        const recover_req: RecoverRequest = { email };
        const res = await authHander.recover(recover_req);
        if (res.status_code == 200) {
        }
        else {
        }
    }
})