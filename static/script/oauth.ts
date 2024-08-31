import { OauthURL, OauthRequest, Response } from "./type.js";
import { apiCall } from "./util.js";

export class OauthHandler {
    async auth_url(provider: string): Promise<Response> {
        const data: OauthURL = {
            provider: provider,
            client_url: "/pages/dashboard"
        }
        try {
            const response = await apiCall("/oauth2", data, "POST");
            return response;
        } catch (error) {
            throw new Error(error);
        }
    }

    async login(): Promise<Response> {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get("code");
        const state = urlParams.get("state");
        const error = urlParams.get("error");
        const error_description = urlParams.get("error_description");
        const data: OauthRequest = {
            code, state, error, error_description
        }
        try {
            const response = await apiCall("/oauth2/callback", data, "POST");
            return response;
        } catch (error) {
            throw new Error(error);
        }
    }
}
