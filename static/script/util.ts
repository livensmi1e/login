import { Response } from "./type.js";

const BACKEND_BASE_URL: string = "https://localhost:8000/api/v1"

export async function apiCall(endpoint: string, body: object, method: string = "GET"): Promise<Response> {
    const URL: string = BACKEND_BASE_URL + endpoint
    try {
        const response = await fetch(URL, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body),
            credentials: "include"
        });
        const jsonBody = response.json()
        return jsonBody
    } catch (error) {
        throw new Error(error)
    }
}

const passwordElement = document.getElementById("register-pass") as HTMLInputElement;
const confirmPasswordElement = document.getElementById("register-confirm-pass") as HTMLInputElement;

export function clearPasswordFields(): void {
    if (passwordElement) passwordElement.value = "";
    if (confirmPasswordElement) confirmPasswordElement.value = "";
}