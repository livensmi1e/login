var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { AuthHandler } from "./auth";
const passwordElement = document.querySelector(".register-pass");
const confirmPasswordElement = document.querySelector(".register-confirm-pass");
const registerEmailElement = document.querySelector(".register-email");
const registerFormElement = document.querySelector("register-form");
const password = passwordElement ? passwordElement.value : "";
const confirmPassword = confirmPasswordElement ? confirmPasswordElement.value : "";
const registerEmail = registerEmailElement ? registerEmailElement.value : "";
export function getPasswordFields() {
    return { password, confirmPassword };
}
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
        console.log(registerEmail);
        const user = {
            email: registerEmail,
            password: password,
            comfirmPasword: confirmPassword
        };
        yield authHandler.register(user);
    });
});
