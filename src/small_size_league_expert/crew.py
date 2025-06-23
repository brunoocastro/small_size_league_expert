from crewai import LLM, Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, after_kickoff, agent, before_kickoff, crew, task
from crewai.tools import BaseTool
from crewai_tools import MCPServerAdapter

from small_size_league_expert.models import (
    DiscordAnswer,
    Question,
    RankResult,
    RetrieverResult,
)
from small_size_league_expert.settings import Settings

from .tools import WikipediaSearchTool

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
    mcp_tools: list[BaseTool] = []
    mcp_adapter: MCPServerAdapter = None

    def __init__(self):
        """Initialize with choice of LLM provider."""
        self.settings = Settings()

    # Close MCP when the instance is destroyed
    def __del__(self):
        """Cleanup when the instance is destroyed."""
        self.cleanup_mcp_adapter()

    def setup_mcp_tools(self):
        """Setup MCP tools with manual connection lifecycle."""
        if self.settings.MCP_ENDPOINT is None:
            print("⚠️ MCP endpoint is not configured. Skipping MCP tools setup.")
            self.mcp_tools = []
            self.mcp_adapter = None
            return

        if self.mcp_adapter is not None:
            # Check MCP connection
            print(f"🔄 Reusing existing MCP adapter. {self.mcp_adapter}")
            return

        server_params = {
            "url": self.settings.MCP_ENDPOINT,
            "transport": self.settings.MCP_TRANSPORT_TYPE,
        }

        try:
            self.mcp_adapter = MCPServerAdapter(server_params)
            print("🔌 MCP adapter initialized successfully.")
            self.mcp_tools = self.mcp_adapter.tools
        except Exception as e:
            print(f"⚠️ Error initializing MCP tools ({type(e)}): {e}")
            self.cleanup_mcp_adapter()

    def cleanup_mcp_adapter(self):
        """Cleanup MCP adapter with manual disconnection lifecycle."""
        if hasattr(self, "mcp_adapter") and self.mcp_adapter is not None:
            try:
                print("🔌 Disconnecting MCP adapter...")
                self.mcp_adapter.stop()  # Manual disconnection
            except Exception as e:
                print(f"⚠️ Error disconnecting MCP adapter ({type(e)}): {e}")
            finally:
                self.mcp_adapter = None
                self.mcp_tools = []
        else:
            print("🔌 No MCP adapter to clean up. Skipping disconnection.")

    def get_llm(self):
        """Get the appropriate LLM based on the configuration."""
        return LLM(
            model=self.settings.MODEL,
            temperature=0,  # Using this to not hallucinate inside the SSL content
        )

    @agent
    def question_handler(self) -> Agent:
        """Create the language detector and decomposer agent."""
        return Agent(
            config=self.agents_config["question_handler"],
            llm=self.get_llm(),
            verbose=True,
        )

    @agent
    def retriever(self) -> Agent:
        tools = [WikipediaSearchTool()]
        print(
            f"Default tools for retriever agent: {''.join([f'\n- {tool.name}' for tool in tools])}"
        )

        self.setup_mcp_tools()

        if self.mcp_tools and len(self.mcp_tools) > 0:
            print("🔌 Adding MCP tools to retriever agent.")
            print(
                f"Available MCP tools: {''.join([f'\n- {tool.name}' for tool in self.mcp_tools])}"
            )
            tools += self.mcp_tools

        return Agent(
            config=self.agents_config["retriever"],
            llm=self.get_llm(),
            verbose=True,
            tools=tools,
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
            knowledge_sources=[text_source],
        )

    @task
    def question_analysis_task(self) -> Task:
        """Detect language and decompose the question."""
        return Task(
            config=self.tasks_config["question_analysis_task"],
            output_pydantic=Question,
        )

    @task
    def retrieval_task(self) -> Task:
        """Retrieve relevant content."""
        return Task(
            config=self.tasks_config["retrieval_task"],
            output_pydantic=RetrieverResult,
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
                self.question_handler(),
                self.retriever(),
                self.ranker(),
                self.answer_generator(),
            ],
            tasks=[
                self.question_analysis_task(),
                self.retrieval_task(),
                self.ranking_task(),
                self.answer_generation_task(),
            ],
            verbose=True,
            process=Process.sequential,
        )

    @before_kickoff
    def prepare_mcp(self, inputs):
        """Prepare MCP adapter before crew execution."""
        if self.mcp_adapter is None:
            print("🔌 Initializing MCP adapter before crew kickoff...")
            self.setup_mcp_tools()
        else:
            print("🔄 Reusing existing MCP adapter.")
        return inputs

    @after_kickoff
    def cleanup_mcp(self, result):
        """Cleanup MCP adapter after crew execution."""
        self.cleanup_mcp_adapter()
        return result
