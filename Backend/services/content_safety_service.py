import re

# Checks text against the configured blocked content.
class ContentSafetyService:

    def __init__(self, blocked_content: dict[str,list[str]]):
        self.blocked_content = blocked_content

    def contains_blocked_content(self, text: str) -> bool:
        
        #Normalize the text into lowercase words for comparison.
        text_words = re.findall(r"\b\w+\b", text.lower())

        #Check each configured category for blocked words. 
        for category, blocked_words in self.blocked_content.items():
            for word in blocked_words:
                if word in blocked_words:
                    if word.lower() in text_words:
                        return True
        return False