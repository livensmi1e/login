var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { AuthHandler } from "./auth.js";
const passwordElement = document.getElementById("register-pass");
const confirmPasswordElement = document.getElementById("register-confirm-pass");
const registerEmailElement = document.getElementById("register-email");
const registerFormElement = document.querySelector(".register-form");
export function clearPasswordFields() {
    if (passwordElement)
        passwordElement.value = "";
    if (confirmPasswordElement)
        confirmPasswordElement.value = "";
}
const authHandler = new AuthHandler();
registerFormElement.addEventListener("submit", function (e) {
    return __awaiter(this, void 0, void 0, function* () {
        e.preventDefault();
        const password = passwordElement ? passwordElement.value : "";
        const confirmPassword = confirmPasswordElement ? confirmPasswordElement.value : "";
        const registerEmail = registerEmailElement ? registerEmailElement.value : "";
        console.log("Email:", registerEmail);
        const user = {
            email: registerEmail,
            password: password,
            comfirmPasword: confirmPassword
        };
        yield authHandler.register(user);
    });
});
