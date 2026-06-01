"""CTB Manager session management with CSRF token handling."""
import json
import os
from typing import Optional
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CTBSession:
    """Manages authenticated session with CTB Manager."""

    def __init__(self, manager_ip: str, username: str, password: str):
        """Initialize session with credentials."""
        self.manager_ip = manager_ip
        self.username = username
        self.password = password
        self.csrftoken = ""
        self.client = requests.Session()
        self.client.verify = False

        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": manager_ip,
            "X-CSRFToken": "",
            "Referer": f"https://{manager_ip}/login",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    def login(self) -> bool:
        """Establish session and authenticate to CTB Manager."""
        login_url = f"https://{self.manager_ip}/api-v1/session"
        status_url = f"https://{self.manager_ip}/api-v1/install/status"

        # Initial requests to get CSRF token
        self.client.get(status_url)
        self.client.get(login_url)

        # Authenticate
        login_data = {"username": self.username, "password": self.password}
        self.headers["Host"] = self.manager_ip
        self.headers["Referer"] = f"https://{self.manager_ip}/login"

        response = self.client.post(
            login_url,
            data=json.dumps(login_data),
            headers=self.headers,
            verify=False
        )

        if response.status_code in (200, 201):
            self.csrftoken = response.cookies.get('csrftoken', '')
            self.headers["X-CSRFToken"] = self.csrftoken
            return True
        return False

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make authenticated request with auto-retry on auth failure."""
        kwargs['headers'] = self.headers
        kwargs['verify'] = False

        response = self.client.request(method, url, **kwargs)

        # Auto-reauth on 401/403
        if response.status_code in (401, 403):
            if self.login():
                kwargs['headers'] = self.headers
                response = self.client.request(method, url, **kwargs)

        return response

    def get_nodes(self) -> requests.Response:
        """Retrieve broker nodes available in CTB Manager."""
        url = f"https://{self.manager_ip}/api-v1/nodes/"
        return self._request('GET', url)

    def get_input_types(self) -> requests.Response:
        """Retrieve supported input types for CTB Manager."""
        url = f"https://{self.manager_ip}/api-v1/input-types/"
        return self._request('GET', url)

    def get_inputs(self, input_id: Optional[str] = None) -> requests.Response:
        """Retrieve inputs; optionally filters by specific input ID."""
        if input_id:
            url = f"https://{self.manager_ip}/api-v1/inputs/{input_id}/"
        else:
            url = f"https://{self.manager_ip}/api-v1/inputs/"
        return self._request('GET', url)

    def get_outputs(self, output_id: Optional[str] = None) -> requests.Response:
        """Retrieve outputs; optionally filters by specific output ID."""
        if output_id:
            url = f"https://{self.manager_ip}/api-v1/outputs/{output_id}/"
        else:
            url = f"https://{self.manager_ip}/api-v1/outputs/"
        return self._request('GET', url)

    def get_subscriptions(self) -> requests.Response:
        """Retrieve all subscriptions."""
        url = f"https://{self.manager_ip}/api-v1/subscriptions/"
        return self._request('GET', url)

    def create_input(self, name: str, node: int, port: int,
                     input_type: str = "udp_listener",
                     track_exporter_disabled: bool = False) -> requests.Response:
        """Create a new input on the specified broker node."""
        url = f"https://{self.manager_ip}/api-v1/inputs/"
        data = json.dumps({
            "name": name,
            "node": node,
            "input_type": input_type,
            "port": port,
            "track_exporter_disabled": track_exporter_disabled
        })
        return self._request('POST', url, data=data)

    def create_output(self, name: str, node: int, address: str, port: int,
                      output_type: str = "udp",
                      dcd_enabled: bool = False) -> requests.Response:
        """Create a new output (destination) on the specified broker node."""
        url = f"https://{self.manager_ip}/api-v1/outputs/"
        data = json.dumps({
            "name": name,
            "node": node,
            "output_type": output_type,
            "address": address,
            "port": port,
            "dcd_enabled": dcd_enabled
        })
        return self._request('POST', url, data=data)

    def create_subscription(self, source: int, destination: int,
                            subnets: Optional[list] = None) -> requests.Response:
        """Create a subscription linking an input to an output."""
        url = f"https://{self.manager_ip}/api-v1/subscriptions/"
        data = json.dumps({
            "source": source,
            "destination": destination,
            "subnets": subnets or []
        })
        return self._request('POST', url, data=data)


def create_session_from_env() -> CTBSession:
    """Create CTBSession from environment variables."""
    manager_ip = os.getenv("CTB_MANAGER_IP")
    username = os.getenv("CTB_USERNAME")
    password = os.getenv("CTB_PASSWORD")

    if not all([manager_ip, username, password]):
        raise ValueError(
            "Missing required environment variables: "
            "CTB_MANAGER_IP, CTB_USERNAME, CTB_PASSWORD"
        )

    session = CTBSession(manager_ip, username, password)
    if not session.login():
        raise RuntimeError(f"Failed to authenticate to CTB Manager at {manager_ip}")

    return session
