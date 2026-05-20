import random
from responses import penisJoke_words
from responses import penisJoke_responses
from responses import curse_words
from responses import curse_responses
from responses import creator_responses
from responses import love_words
from responses import love_responses
from responses import random_responses
from responses import berry_responses
from responses import random_reply_responses
from responses import random_joke_words

class ChatService:

    def is_berry_mentioned(self, content: str) -> bool:
        content = content.lower()

        return any(
            word in content
            for word in ["berry", "berry flames"]
        )
    
    def get_response(self, content: str, self_mentioned: bool):

        content = content.lower()

        # Question response
        if self_mentioned and "?" in content:
            return random.choice(random_reply_responses)

        # Love response
        if self_mentioned and any(word in content for word in love_words):
            return random.choice(love_responses)
        
        # Patting response
        if "pats berry" in content or "pat berry" in content:
            return "eep!"

        # Joke response
        if self_mentioned and any(word in content for word in random_joke_words) and "joke" in content:
            joke = self.joke_service.get_joke()
            if joke:
                return joke

        # Callout response
        if self_mentioned and content in ["berry", "berry!"]:
            return random.choice(berry_responses)

        return None