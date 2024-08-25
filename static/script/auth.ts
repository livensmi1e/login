import { CreateUser, CreateUserRequest } from "./type";
import { apiCall } from "./api";
import { clearPasswordFields } from "./index";

export class AuthHandler {
    constructor() { }
    login() {

    }

    async register(createUser: CreateUser) {
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
            if (res.status_code == 201) {
                console.log(res)
            }
            else {
                alert("Create user failed!")
            }
        } catch (error) {
            alert("Create user failed!")
        }
    }
}