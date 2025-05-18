from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import MCPServerAdapter

from small_size_league_promoter.models import QuestionAnswer
from small_size_league_promoter.settings import Settings

from .tools import WikipediaSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Create a text file knowledge source
text_source = TextFileKnowledgeSource(file_paths=["content_description.txt"])


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
            temperature=0.1,  # Using this to not hallucinate inside the SSL content
        )

    # @agent
    # def analyst(self) -> Agent:
    #     """Create the analyst agent."""
    #     return Agent(
    #         config=self.agents_config["analyst"],
    #         llm=self.get_llm(),
    #         verbose=True,
    #         knowledge_sources=[text_source],
    #     )

    # @agent
    # def tdp_researcher(self) -> Agent:
    #     """Create the TDP researcher agent."""
    #     return Agent(
    #         config=self.agents_config["tdp_researcher"],
    #         agent_ops_agent_name="tdp_researcher",
    #         verbose=True,
    #         llm=self.get_llm(),
    #         tools=[TDPSearchTool(), WikipediaSearchTool()],
    #     )

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

    # @agent
    # def writer(self) -> Agent:
    #     """Create the writer agent."""
    #     return Agent(
    #         config=self.agents_config["writer"],
    #         verbose=True,
    #         llm=self.get_llm(),
    #         knowledge_sources=[text_source],
    #     )

    # @agent
    # def editor(self) -> Agent:
    #     """Create the editor agent."""
    #     return Agent(
    #         config=self.agents_config["editor"],
    #         verbose=True,
    #         llm=self.get_llm(),
    #     )

    @agent
    def classifier(self) -> Agent:
        """Create the classifier agent."""
        return Agent(
            config=self.agents_config["classifier"],
            llm=self.get_llm(),
            verbose=True,
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

    # @task
    # def classification_task(self) -> Task:
    #     """Classify if the question is SSL-related."""
    #     return Task(
    #         config=self.tasks_config["classification_task"],
    #     )

    @task
    def language_detection_decomposition_task(self) -> Task:
        """Detect language and decompose the question."""
        return Task(
            config=self.tasks_config["language_detection_decomposition_task"],
        )

    @task
    def retrieval_task(self) -> Task:
        """Retrieve relevant content."""
        return Task(
            config=self.tasks_config["retrieval_task"],
        )

    @task
    def ranking_task(self) -> Task:
        """Rank and filter the content."""
        return Task(
            config=self.tasks_config["ranking_task"],
        )

    @task
    def answer_generation_task(self) -> Task:
        """Generate the final answer in Markdown for Discord."""
        return Task(
            config=self.tasks_config["answer_generation_task"],
            output_pydantic=QuestionAnswer,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SSL Q&A crew for Discord."""
        return Crew(
            agents=[
                self.classifier(),
                self.language_decomposer(),
                self.retriever(),
                self.ranker(),
                self.answer_generator(),
            ],
            tasks=[
                # self.classification_task(),
                self.language_detection_decomposition_task(),
                self.retrieval_task(),
                self.ranking_task(),
                self.answer_generation_task(),
            ],
            verbose=True,
            process=Process.sequential,
            memory=True,
        )
