from urlscan.client import BASE_URL, USER_AGENT, BaseClient, TimeoutTypes

from .livescan import LiveScan
from .subscription import Subscription


class Pro(BaseClient):
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        user_agent: str = USER_AGENT,
        trust_env: bool = False,
        timeout: TimeoutTypes = 60,
        proxy: str | None = None,
        verify: bool = True,
        retry: bool = False,
    ):
        """
        Args:
            api_key (str): Your urlscan.io API key.
            base_url (str, optional): Base URL. Defaults to BASE_URL.
            user_agent (str, optional): User agent. Defaults to USER_AGENT.
            trust_env (bool, optional): Enable or disable usage of environment variables for configuration. Defaults to False.
            timeout (TimeoutTypes, optional): timeout configuration to use when sending request. Defaults to 60.
            proxy (str | None, optional): Proxy URL where all the traffic should be routed. Defaults to None.
            verify (bool, optional): Either `True` to use an SSL context with the default CA bundle, `False` to disable verification. Defaults to True.
            retry (bool, optional): Whether to use automatic X-Rate-Limit-Reset-After HTTP header based retry. Defaults to False.
        """
        super().__init__(
            api_key,
            base_url=base_url,
            user_agent=user_agent,
            trust_env=trust_env,
            timeout=timeout,
            proxy=proxy,
            verify=verify,
            retry=retry,
        )

        self.livescan = LiveScan(
            api_key=api_key,
            base_url=base_url,
            user_agent=user_agent,
            trust_env=trust_env,
            timeout=timeout,
            proxy=proxy,
            verify=verify,
            retry=retry,
        )

        self.subscription = Subscription(
            api_key=api_key,
            base_url=base_url,
            user_agent=user_agent,
            trust_env=trust_env,
            timeout=timeout,
            proxy=proxy,
            verify=verify,
            retry=retry,
        )
