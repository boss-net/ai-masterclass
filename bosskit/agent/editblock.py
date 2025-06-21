from bosskit.editblock import EditBlockPrompts

from .agent import Agent


class EditBlockAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_prompts = EditBlockPrompts()
