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

"""Crisis agent for Sei therapist that handles emergency situations."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from sei_therapist.sub_agents.crisis import prompt
from sei_therapist.tools.memory import memorize

# Sub-agents for crisis assessment and safety planning
assess_crisis_agent = Agent(
    model="gemini-2.0-flash",
    name="assess_crisis_agent",
    description="Assesses crisis level and provides appropriate resources",
    instruction=prompt.ASSESS_CRISIS_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

safety_plan_agent = Agent(
    model="gemini-2.0-flash",
    name="safety_plan_agent",
    description="Creates a safety plan for crisis situations",
    instruction=prompt.SAFETY_PLAN_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

# Main crisis agent
crisis_agent = Agent(
    model="gemini-2.0-flash",
    name="crisis_agent",
    description="Handles crisis situations with immediate safety focus",
    instruction=prompt.CRISIS_AGENT_INSTR,
    tools=[memorize, AgentTool(agent=assess_crisis_agent), AgentTool(agent=safety_plan_agent)],
)