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

"""Main Sei therapist agent coordinating therapeutic sub-agents."""

from google.adk.agents import Agent

from sei_therapist import prompt
from sei_therapist.sub_agents.onboarding.agent import onboarding_agent
from sei_therapist.sub_agents.greeting.agent import greeting_agent
from sei_therapist.sub_agents.farewell.agent import farewell_agent
from sei_therapist.sub_agents.crisis.agent import crisis_agent
from sei_therapist.sub_agents.therapeutic.agent import therapeutic_agent
from sei_therapist.sub_agents.treatment.agent import treatment_agent

from sei_therapist.tools.memory import _load_default_profile

# Root Sei therapist agent that coordinates all sub-agents
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="sei_therapist",
    description="Sei is an empathetic AI therapist that coordinates personalized therapeutic approaches",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        onboarding_agent,
        greeting_agent,
        farewell_agent,
        crisis_agent,
        therapeutic_agent,
        treatment_agent,
    ],
    before_agent_callback=_load_default_profile,
)