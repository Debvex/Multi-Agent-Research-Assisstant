# MultiAgentResearchAssisstant Crew

This is a Multi Agent Research Assistant implemented through Crew AI, it involves researcher, reviewer, analyst, summarizer agents and custom bag of tools according to their needs to be used to finally export a output.md file based on any topic which is given as a input (presently hardcoded in the main.py file) to be researched on.

<img width="1919" height="1035" alt="Screenshot 2026-08-12 163521" src="https://github.com/user-attachments/assets/4f7b0e82-2c45-497a-836a-abf637bfdc0c" />

<img width="1919" height="1037" alt="image" src="https://github.com/user-attachments/assets/413cfddd-ff78-4339-98e2-04226358264b" />


## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/multi_agent_research_assisstant/config/agents.yaml` to define your agents
- Modify `src/multi_agent_research_assisstant/config/tasks.yaml` to define your tasks
- Modify `src/multi_agent_research_assisstant/crew.py` to add your own logic, tools and specific args
- Modify `src/multi_agent_research_assisstant/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the Multi_Agent_Research_Assisstant Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The Multi_Agent_Research_Assisstant Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.


