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

"""Treatment agent for Sei therapist that handles therapeutic planning."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from sei_therapist.sub_agents.treatment import prompt
from sei_therapist.tools.memory import memorize, create_treatment_plan, add_user_concern

# Sub-agent for creating treatment plans
create_plan_agent = Agent(
    model="gemini-2.0-flash",
    name="create_plan_agent",
    description="Creates structured treatment plans based on user needs",
    instruction=prompt.CREATE_PLAN_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

# Main treatment planning agent
treatment_agent = Agent(
    model="gemini-2.0-flash",
    name="treatment_agent",
    description="Handles treatment planning and therapeutic goal setting",
    instruction=prompt.TREATMENT_AGENT_INSTR,
    tools=[memorize, create_treatment_plan, add_user_concern, AgentTool(agent=create_plan_agent)],
)