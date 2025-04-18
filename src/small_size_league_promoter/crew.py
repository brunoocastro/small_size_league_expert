from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task

from small_size_league_promoter.models import Article
from small_size_league_promoter.settings import Settings

from .tools import TDPSearchTool, WikipediaSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Create a text file knowledge source
text_source = TextFileKnowledgeSource(file_paths=["full_ssl_website.txt"])


@CrewBase
class SmallSizeLeaguePromoter:
    """SmallSizeLeaguePromoter crew for RoboCup SSL article generation"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    def __init__(self):
        """Initialize with choice of LLM provider."""
        self.settings = Settings()

    def get_llm(self):
        """Get the appropriate LLM based on the configuration."""
        return LLM(
            model=self.settings.MODEL,
            temperature=0.3,  # Using this to not hallucinate inside the SSL content
        )

    @agent
    def analyst(self) -> Agent:
        """Create the analyst agent."""
        return Agent(
            config=self.agents_config["analyst"],
            llm=self.get_llm(),
            verbose=True,
            knowledge_sources=[text_source],
        )

    @agent
    def tdp_researcher(self) -> Agent:
        """Create the TDP researcher agent."""
        return Agent(
            config=self.agents_config["tdp_researcher"],
            agent_ops_agent_name="tdp_researcher",
            verbose=True,
            llm=self.get_llm(),
            tools=[TDPSearchTool(), WikipediaSearchTool()],
        )

    # TODO: Add website content repository agent that connects to the MCP
    # @agent
    # def website_content_repository(self) -> Agent:
    #     """Create the website content repository agent."""
    #     return Agent(
    #         config=self.agents_config["website_content_repository"],
    #         verbose=True,
    #         llm=self.get_llm(),
    #         tools=[],
    #         knowledge_sources=[text_source],
    #     )

    @agent
    def writer(self) -> Agent:
        """Create the writer agent."""
        return Agent(
            config=self.agents_config["writer"],
            verbose=True,
            llm=self.get_llm(),
            knowledge_sources=[text_source],
        )

    @agent
    def editor(self) -> Agent:
        """Create the editor agent."""
        return Agent(
            config=self.agents_config["editor"],
            verbose=True,
            llm=self.get_llm(),
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyst_task(self) -> Task:
        """Create the analyst task."""
        return Task(
            config=self.tasks_config["analyst_task"],
        )

    @task
    def research_task(self) -> Task:
        """Create the research task with multiple agents."""
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def writing_task(self) -> Task:
        """Create the writing task."""
        return Task(
            config=self.tasks_config["writing_task"],
        )

    @task
    def editing_task(self) -> Task:
        """Create the editing task."""
        return Task(config=self.tasks_config["editing_task"], output_pydantic=Article)

    @crew
    def crew(self) -> Crew:
        """Creates the RoboCup SSL article generation crew."""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            verbose=True,
            process=Process.sequential,
            memory=True,
        )
