__all__ = ("fake",)

from faker import Faker

Faker.seed('test_2')

fake = Faker()
