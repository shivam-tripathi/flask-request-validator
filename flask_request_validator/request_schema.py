class RequestSchema:
    def __init__(self, schema):
        self.schema = schema

    def get(self, field):
        return self.schema.get(field) if self.schema is not None else None

    def items(self):
        return self.schema.items() if self.schema is not None else []

    def __str__(self):
        return str(self.schema)
