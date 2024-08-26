import { Response } from "./type.js";

const BACKEND_BASE_URL: string = "http://localhost:8000/api/v1"

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
        console.error("Fetch error:", error)
        throw new Error("Fetch error")
    }
}