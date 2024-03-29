"""Create fake models for tests and seeding dev DB."""
from faker import Factory as FakerFactory
import factory
import random

from db_kursach_s2.model import BirthAct, Person, DeathAct, MarriageAct
from db_kursach_s2.model.user import NormalUser, User, AdminUser
from db_kursach_s2.db import db
from jetkit.db import Session

faker: FakerFactory = FakerFactory.create()
DEFAULT_NORMAL_USER_EMAIL = "test@test.test"
DEFAULT_PASSWORD = "testo"


def seed_db():
    # seed DB with factories here
    # https://pytest-factoryboy.readthedocs.io/en/latest/#model-fixture

    # default normal user
    if not User.query.filter_by(email=DEFAULT_NORMAL_USER_EMAIL).one_or_none():
        # add default user for testing
        db.session.add(
            AdminUserFactory.create(
                email=DEFAULT_NORMAL_USER_EMAIL, password=DEFAULT_PASSWORD
            )
        )
        print(
            f"Created default user with email {DEFAULT_NORMAL_USER_EMAIL} "
            f"with password '{DEFAULT_PASSWORD}'"
        )

    db.session.add_all(BirthActFactory.create_batch(5))
    db.session.add_all(DeathActFactory.create_batch(5))
    db.session.add_all(MarriageActFactory.create_batch(5))

    db.session.commit()
    print("Database seeded.")


class SQLAFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Use a scoped session when creating factory models."""

    class Meta:
        abstract = True
        sqlalchemy_session = Session


class UserFactoryFactory(SQLAFactory):
    class Meta:
        abstract = True

    dob = factory.LazyAttribute(lambda x: faker.simple_profile()["birthdate"])
    name = factory.LazyAttribute(lambda x: faker.name())
    password = DEFAULT_PASSWORD
    avatar_url = factory.LazyAttribute(
        lambda x: f"https://placem.at/people?w=200&txt=0&random={random.randint(1, 100000)}"
    )


class NormalUserFactory(UserFactoryFactory):
    class Meta:
        model = NormalUser

    email = factory.Sequence(lambda n: f"normaluser.{n}@example.com")


class AdminUserFactory(UserFactoryFactory):
    class Meta:
        model = AdminUser

    email = factory.Sequence(lambda n: f"admin.{n}@example.com")


class PersonFactory(SQLAFactory):
    class Meta:
        model = Person

    first_name = factory.LazyFunction(faker.first_name)
    last_name = factory.LazyFunction(faker.last_name)
    address = factory.LazyFunction(faker.address)
    date_of_birth = factory.LazyFunction(faker.past_date)
    passport_series = factory.LazyFunction(faker.word)
    passport_number = factory.LazyFunction(faker.word)


class ActFactory(SQLAFactory):
    class Meta:
        abstract = True

    issued_by = factory.LazyFunction(faker.random_int)
    issued_at = factory.LazyFunction(faker.past_date)
    created_by = factory.SubFactory(NormalUserFactory)


class BirthActFactory(ActFactory):
    class Meta:
        model = BirthAct

    father = factory.SubFactory(PersonFactory)
    mother = factory.SubFactory(PersonFactory)
    child = factory.SubFactory(PersonFactory)

    birthplace = factory.LazyFunction(faker.address)
    child_nationality = "Ukrainian"


class DeathActFactory(ActFactory):
    class Meta:
        model = DeathAct

    deceased = factory.SubFactory(PersonFactory)
    deceased_at = factory.LazyFunction(faker.past_date)
    deceased_age = factory.LazyFunction(faker.random_int)
    place_of_demise = factory.LazyFunction(faker.address)


class MarriageActFactory(ActFactory):
    class Meta:
        model = MarriageAct

    bride = factory.SubFactory(PersonFactory)
    groom = factory.SubFactory(PersonFactory)
    bride_last_name = factory.LazyFunction(faker.word)
    groom_last_name = factory.LazyFunction(faker.word)
    wed_at = factory.LazyFunction(faker.past_date)
