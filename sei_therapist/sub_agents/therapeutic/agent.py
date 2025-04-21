# Copyright 2025 Sei AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Therapeutic agents with specialized approaches for Sei therapist."""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from sei_therapist.sub_agents.therapeutic import prompt
from sei_therapist.tools.memory import remember_insight

# Specialized therapeutic approach agents
cbt_agent = Agent(
    model="gemini-2.0-flash",
    name="cbt_agent",
    description="Applies Cognitive Behavioral Therapy principles",
    instruction=prompt.CBT_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="cbt_perspective",
)

psychoanalysis_agent = Agent(
    model="gemini-2.0-flash",
    name="psychoanalysis_agent",
    description="Explores deeper patterns using psychodynamic principles",
    instruction=prompt.PSYCHOANALYSIS_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="psychoanalytic_perspective",
)

motivational_agent = Agent(
    model="gemini-2.0-flash",
    name="motivational_agent",
    description="Focuses on strengths and motivation for change",
    instruction=prompt.MOTIVATIONAL_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="motivational_perspective",
)

faith_based_agent = Agent(
    model="gemini-2.0-flash",
    name="faith_based_agent",
    description="Integrates Christian principles with therapeutic approaches",
    instruction=prompt.FAITH_BASED_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="faith_based_perspective",
)

# Create parallel agent to run multiple therapeutic approaches simultaneously
# To this:
parallel_consultation = ParallelAgent(
    name="parallel_consultation",
    sub_agents=[cbt_agent, psychoanalysis_agent, motivational_agent, faith_based_agent],
)

# Integration agent to synthesize the perspectives
integration_agent = Agent(
    model="gemini-2.0-flash",
    name="integration_agent",
    description="Synthesizes insights from different therapeutic perspectives",
    instruction=prompt.INTEGRATION_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="integrated_response",
)

# Combine into sequential process (parallel consultation then integration)
therapeutic_process = SequentialAgent(
    name="therapeutic_process",
    description="Processes therapeutic perspectives and integrates them",
    sub_agents=[parallel_consultation, integration_agent],
)

# Main therapeutic agent
therapeutic_agent = Agent(
    model="gemini-2.0-flash",
    name="therapeutic_agent",
    description="Provides core therapeutic experience through integrated approaches",
    instruction=prompt.THERAPEUTIC_AGENT_INSTR,
    tools=[remember_insight, AgentTool(agent=therapeutic_process)],
)