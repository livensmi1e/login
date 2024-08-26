import { CreateUser, User, Response } from "./type.js";
import { apiCall } from "./util.js";
import { clearPasswordFields } from "./index.js";

export class AuthHandler {
    constructor() { }
    async login(loginUser: User): Promise<Response> {
        try {
            const res = await apiCall("/auth/login", loginUser, "POST");
            return res;

        } catch (error) {
            throw new Error(error);
        }
    }

    async register(createUser: CreateUser): Promise<Response> {
        if (createUser.comfirmPasword != createUser.password) {
            clearPasswordFields();
            return;
        }
        const user: User = {
            email: createUser.email,
            password: createUser.password
        }
        try {
            const res = await apiCall("/auth/register", user, "POST");
            return res;
        } catch (error) {
            throw new Error(error);
        }
    }
}