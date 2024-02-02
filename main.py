from peewee import PostgresqlDatabase, Model, CharField, ProgrammingError
from playhouse.postgres_ext import ArrayField
import bcrypt

psql_db = PostgresqlDatabase("postgres", host="localhost", port=5432)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = psql_db


class User(BaseModel):
    username = CharField()
    password_hash = CharField()
    prev_password_hashes = ArrayField(CharField, null=True)


try:
    psql_db.drop_tables(User)
except ProgrammingError:
    # don't need to drop
    pass

psql_db.create_tables([User])


def hash_pwd(pwd) -> bytes:
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())


pass_hashes = [hash_pwd(str(i)).decode() for i in range(0, 5)]

user = User.create(
    username="test_user",
    password_hash=hash_pwd("password"),
    prev_password_hashes=pass_hashes,
)

saved_user = User.get_by_id(user.id)

print(f"{saved_user.prev_password_hashes=}")
print(f"{saved_user.password_hash=}")

saved_user.prev_password_hashes.insert(0, hash_pwd("hi"))
saved_user.save()
