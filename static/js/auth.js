var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { apiCall } from "./util.js";
import { clearPasswordFields } from "./index.js";
export class AuthHandler {
    constructor() { }
    login() {
    }
    register(createUser) {
        return __awaiter(this, void 0, void 0, function* () {
            if (createUser.comfirmPasword != createUser.password) {
                clearPasswordFields();
                return;
            }
            const user = {
                email: createUser.email,
                password: createUser.password
            };
            try {
                const res = yield apiCall("/auth/register", user, "POST");
                return res;
            }
            catch (error) {
                alert(`Create user failed! Reason: ${error}`);
            }
        });
    }
}
