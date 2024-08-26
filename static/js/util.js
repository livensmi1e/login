var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const BACKEND_BASE_URL = "http://localhost:8000/api/v1";
export function apiCall(endpoint_1, body_1) {
    return __awaiter(this, arguments, void 0, function* (endpoint, body, method = "GET") {
        const URL = BACKEND_BASE_URL + endpoint;
        try {
            const response = yield fetch(URL, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body),
                credentials: "include"
            });
            const jsonBody = response.json();
            return jsonBody;
        }
        catch (error) {
            throw new Error(error);
        }
    });
}
