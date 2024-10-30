class BasicAssistant:

    @staticmethod
    def get_prompt() -> str:
        return """
        You are a helpful assistant.
        If you don't know the answer, just say: I don't know
        """

class CorporateCreditAssistant:

    @staticmethod
    def get_prompt(docs: str) -> str:
        return """
        You are a helpful assistant. You answer questions about corporate credit ratings. 
        But you only answer based on knowledge I'm providing you. You don't use your internal 
        knowledge and you don't make thins up.
        If you don't know the answer, just say: I don't know
        --------------------
        The data:
        """+str(docs)+"""
        """
