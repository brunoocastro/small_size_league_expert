from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import MCPServerAdapter

from small_size_league_expert.models import (
    DiscordAnswer,
    Question,
    RankResult,
    RetrieverResult,
)
from small_size_league_expert.settings import Settings

from .tools import WikipediaSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Create a text file knowledge source
text_source = TextFileKnowledgeSource(file_paths=["content_description.txt"])


@CrewBase
class SmallSizeLeagueExpert:
    """SmallSizeLeagueExpert crew for RoboCup SSL article generation"""

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
            temperature=0,  # Using this to not hallucinate inside the SSL content
        )

    @agent
    def language_decomposer(self) -> Agent:
        """Create the language detector and decomposer agent."""
        return Agent(
            config=self.agents_config["language_decomposer"],
            llm=self.get_llm(),
            verbose=True,
        )

    @agent
    def retriever(self) -> Agent:
        """Create the retriever agent."""
        server_params = {
            "url": "http://localhost:8000/sse",
        }
        with MCPServerAdapter(server_params) as MCPTools:
            print(f" Loaded {len(MCPTools)} MCP Tools from {server_params['url']}")
            return Agent(
                config=self.agents_config["retriever"],
                llm=self.get_llm(),
                verbose=True,
                tools=MCPTools + [WikipediaSearchTool()],
            )

    @agent
    def ranker(self) -> Agent:
        """Create the ranker agent."""
        return Agent(
            config=self.agents_config["ranker"],
            llm=self.get_llm(),
            verbose=True,
        )

    @agent
    def answer_generator(self) -> Agent:
        """Create the answer generator agent."""
        return Agent(
            config=self.agents_config["answer_generator"],
            llm=self.get_llm(),
            verbose=True,
        )

    @task
    def language_detection_decomposition_task(self) -> Task:
        """Detect language and decompose the question."""
        return Task(
            config=self.tasks_config["language_detection_decomposition_task"],
            output_pydantic=Question,
        )

    @task
    def retrieval_task(self) -> Task:
        """Retrieve relevant content."""
        return Task(
            config=self.tasks_config["retrieval_task"],
            expected_output=RetrieverResult,
        )

    @task
    def ranking_task(self) -> Task:
        """Rank and filter the content."""
        return Task(
            config=self.tasks_config["ranking_task"],
            output_pydantic=RankResult,
        )

    @task
    def answer_generation_task(self) -> Task:
        """Generate the final answer in Markdown for Discord."""
        return Task(
            config=self.tasks_config["answer_generation_task"],
            output_pydantic=DiscordAnswer,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SSL Q&A crew for Discord."""
        return Crew(
            agents=[
                self.language_decomposer(),
                self.retriever(),
                self.ranker(),
                self.answer_generator(),
            ],
            tasks=[
                self.language_detection_decomposition_task(),
                self.retrieval_task(),
                self.ranking_task(),
                self.answer_generation_task(),
            ],
            verbose=True,
            process=Process.sequential,
        )
