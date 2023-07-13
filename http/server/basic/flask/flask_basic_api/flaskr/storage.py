class Storage:
    def __init__(self, db) -> None:
        self.db = db

    def insert(self, entity, item):
        try:
            if not item:
                raise Exception(f"invalid {entity}")
            self.db.session.add(entity(**item))
            self.db.session.commit()
            return 204
        except Exception as e:
            print(repr(e))
            return 400

    def update(self, entity, id, item):
        try:
            if not item:
                raise Exception(f"invalid {entity}")

            if old_item := entity.query.get(id):
                self.db.session.merge(entity(id=old_item.id, **item))
                self.db.session.commit()
                return 204
            else:
                return 404
        except Exception as e:
            print(repr(e))
            return 400

    def delete(self, entity, id):
        try:
            if old_item := entity.query.get(id):
                self.db.session.delete(old_item)
                self.db.session.commit()
                return 204
            else:
                return 404
        except Exception as e:
            print(repr(e))
            return 400
