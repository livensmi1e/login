import { CreateUser, CreateUserRequest, Response } from "./type.js";
import { apiCall } from "./util.js";
import { clearPasswordFields } from "./index.js";

export class AuthHandler {
    constructor() { }
    login() {

    }

    async register(createUser: CreateUser): Promise<Response> {
        if (createUser.comfirmPasword != createUser.password) {
            clearPasswordFields();
            return;
        }
        const user: CreateUserRequest = {
            email: createUser.email,
            password: createUser.password
        }
        try {
            const res = await apiCall("/auth/register", user, "POST");
            return res;
        } catch (error) {
            alert(`Create user failed! Reason: ${error}`)
        }
    }
}