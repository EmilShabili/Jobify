import random
import string


class CodeGenerator:
    @classmethod
    def create_activation_link_code(cls, size, model_):
        new_code = cls.code_slug_only_number_generator(size=size)
        qs_exists = model_.objects.filter(activation_code=new_code).exists()
        return cls.code_slug_only_number_generator(size, model_) if qs_exists else new_code

    @staticmethod
    def code_slug_only_number_generator(size, chars=string.digits):
        return "".join(random.choice(chars) for _ in range(size))
