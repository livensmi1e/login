import { OauthHandler } from "./oauth.js";

(async () => {
    const oauthHandler = new OauthHandler();
    const res = await oauthHandler.login()
    if ("data" in res) {
        const access_token = res.data.access_token;
        document.cookie = `access_token=${access_token}`
        window.location.href = '/pages/dashboard.html'
    }
    else {
        alert("Error occured, try again");
        window.location.href = '/pages/index.html'
    }
})();