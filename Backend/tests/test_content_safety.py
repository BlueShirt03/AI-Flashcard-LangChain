from Backend.services.content_safety_service import ContentSafetyService
from Backend.config import BLOCKED_CONTENT

# Instance of Content Safety Service class taking in 
# a dictionary of blocked content from application's config.py
safety_service = ContentSafetyService(BLOCKED_CONTENT)

# Print results
# If sentence contains NSFW word result will be true, else result will be false
print(safety_service.contains_blocked_content("Porn is good."))
print(safety_service.contains_blocked_content("I love eating pizza!"))
print(safety_service.contains_blocked_content("Hello There."))
print(safety_service.contains_blocked_content("Look at that ass!"))