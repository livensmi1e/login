import { CreateUser, User, Response, RecoverRequest, PasswordReset } from "./type.js";
import { apiCall } from "./util.js";
import { clearPasswordFields } from "./util.js";

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

    async logout(): Promise<Response> {
        try {
            const res = await apiCall("/auth/logout", {}, "POST");
            return res;
        } catch (error) {
            throw new Error(error);
        }
    }

    async recover(recover_req: RecoverRequest): Promise<Response> {
        try {
            const res = await apiCall("/auth/password-recovery", recover_req, "POST");
            return res;
        } catch (error) {
            throw new Error(error);
        }
    }

    async reset(password_reset: PasswordReset): Promise<Response> {
        try {
            const res = await apiCall("/auth/reset-password", password_reset, "POST");
            return res;
        } catch (error) {
            throw new Error(error);
        }
    }
}