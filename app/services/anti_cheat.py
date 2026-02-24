class AntiCheatService:
    def evaluate(self, answer_time_ms: int) -> dict:
        suspicious = answer_time_ms < 350
        multiplier = 0.5 if suspicious else 1.0
        return {"suspicious": suspicious, "multiplier": multiplier}
