const current_base_url = "https://www.cs.utexas.edu/users/mad/utcs-app-backend/1.1/cgi-bin/utcs.scgi";
const proxy_url = "https://www.txcsmad.com/labstatus/backend-proxy";
const stats_url = "https://www.txcsmad.com/labstatus/stats";
const utcs_js_key = "aS9O0@Ke";
const UTCSBackendService = {
    LAYOUT: 'labs-layout',
    LABS: 'labs',
};

class UTCSBackend {
    constructor(api_key, base_url) {
        this.key = api_key;
        this.base_url = base_url;
    }

    request(service, callback) {
        let url = this.create_url(service);
        let headers = this.create_headers(service);
        return $.ajax({
            url: url,
            success: callback,
            dataType: "json",
            // Headers are causing HTTPS issues
            //headers: headers
        });
    }

    create_url(service) {
        return this.base_url + "?service=" + String(service);
    }

    create_headers(service) {
        const digest = UTCSBackend.makeDigest(String(service), null, this.key);
        return {"authentication": "hmac web:" + digest}
    }

    static makeDigest(service, arg, key) {
        if (arg === null) {
            arg = ""
        }
        const time = (new Date).getTime() / 1000.0;
        const timestamp = Math.floor(Math.round(time) / 30);
        const message = String(service) + String(arg) + String(timestamp);
        const shaObj = new jsSHA("SHA-1", "TEXT");
        shaObj.setHMACKey(key, "TEXT");
        shaObj.update(message);
        const hmac = shaObj.getHMAC("HEX");
        return hmac;
    }
}

class StatsBackend {
    constructor(api_key, base_url) {
        this.key = api_key;
        this.base_url = base_url;
    }

    request(service, callback) {
        let url = this.create_url(service);
        //let headers = this.create_headers(service);
        return $.ajax({
            url: url,
            success: callback,
            dataType: "json",
            // Headers are causing HTTPS issues
            //headers: headers
        });
    }

    create_url(service) {
        return this.base_url;
    }
}



