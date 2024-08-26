export type CreateUser = {
    email: string;
    password: string;
    comfirmPasword: string;
}

export type User = {
    email: string;
    password: string;
}

interface SuccessReponse {
    status_code: number,
    message: string,
    data: any
}

interface ErrorReponse {
    status_code: number,
    error: {
        message: string,
        detail: any
    }
}

export type Response = SuccessReponse | ErrorReponse