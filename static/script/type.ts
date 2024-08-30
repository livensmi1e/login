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

export type OauthRequest = {
    code: string,
    state: string,
    error?: string,
    error_description?: string
}

export type OauthURL = {
    provider: string,
    client_url: string
}