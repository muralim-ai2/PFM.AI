class Anthropic:
    """Needs `pip install anthropic` and ANTHROPIC_API_KEY. `extra` goes straight to messages.create."""

    def __init__(self):
        import anthropic
        self.client, self.tokens = anthropic.Anthropic(), 0

    def complete(self, model, system, prompt, extra=None):
        r = self.client.messages.create(model=model, max_tokens=16000, system=system,
                                        messages=[{"role": "user", "content": prompt}], **(extra or {}))
        self.tokens += r.usage.input_tokens + r.usage.output_tokens
        return "".join(b.text for b in r.content if b.type == "text")
