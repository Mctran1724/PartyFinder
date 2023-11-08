

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "matchmake":
        return "Matchmaking"

    return "Command not understood"
