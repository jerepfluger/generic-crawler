class Response:
    def __init__(self, message, status):
        self.message = message
        self.status = status


class InstagramDetailedResponse:
    def __init__(self, tagging_response, follow_response, like_response, status):
        self.tagging_response = tagging_response
        self.follow_response = follow_response
        self.like_response = like_response
        self.status = status
