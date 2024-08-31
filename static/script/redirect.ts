import { OauthHandler } from "./oauth.js";

(async () => {
    const oauthHandler = new OauthHandler();
    const res = await oauthHandler.login()
    if ("data" in res && res.status_code == 200) {
        window.location.href = '/pages/dashboard.html'
    }
    else {
        alert("Error occured, try again");
        window.location.href = '/pages/index.html'
    }
})();