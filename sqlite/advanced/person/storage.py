from typing import List, Tuple

from pypika import Table
from pypika.dialects import Term


from .model import Person
from storage import storage


class PersonStorage:
    def __init__(self, file: str) -> None:
        self.stor = storage.Storage(file)
        self.tb_persons = Table("tb_persons")

    def insert(self, persons: List[Person] | Person) -> Tuple[int, Exception | None]:
        if isinstance(persons, Person):
            persons = [persons]

        return self.stor.insert(
            self.tb_persons,
            vals=[(p.name, p.age) for p in persons],
        )

    def select_one(self, where: Term | None) -> Tuple[Person | None, Exception | None]:
        row, err = self.select(where=where, limit=1)
        if err or len(row) != 1:
            return None, err
        return row.pop(), None

    def select(
        self,
        where: Term | None = None,
        limit: int | None = None,
    ) -> Tuple[List[Person], Exception | None]:
        rows, err = self.stor.select(
            self.tb_persons,
            where=where,
            limit=limit,
        )

        if err:
            return [], err

        if isinstance(rows, List) and len(rows) == 0:
            return [], None

        try:
            persons = [Person(*r) for r in rows]
        except Exception as e:
            return [], e
        else:
            return persons, None

    def update(
        self,
        person: Person,
        where: Term | List[Term],
    ) -> Tuple[int, Exception | None]:
        if not isinstance(person, Person):
            raise TypeError("person should be Person type")

        return self.stor.update(
            self.tb_persons,
            vals=[
                (self.tb_persons.name, person.name),
                (self.tb_persons.age, person.age),
            ],
            where=where,
        )
