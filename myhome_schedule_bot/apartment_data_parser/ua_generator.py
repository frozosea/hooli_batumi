from abc import ABC
from abc import abstractmethod
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class IUserAgentGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        ...


class UserAgentGenerator(IUserAgentGenerator):
    def generate(self) -> str:
        """this func generates random user agent"""
        software_names = [SoftwareName.WEBKIT.value]
        operating_systems = [OperatingSystem.LINUX.value]

        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                       limit=100)

        # Get list of user agents.
        user_agents = user_agent_rotator.get_user_agents()

        # Get Random User Agent String.
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent