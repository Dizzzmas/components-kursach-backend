from flask_smorest import Blueprint, abort
from jetkit.api import CursorPage, combined_search_by
from smorest_crud import CollectionView, ResourceView

from db_kursach_s2.api.person.schema import PersonSchema
from db_kursach_s2.db import BaseQuery
from db_kursach_s2.model import Act, Person

blp = Blueprint("Person", __name__, url_prefix="/people")


@blp.route("")
class PeopleCollection(CollectionView):
    model = Person
    decorators = []
    list_enabled = True
    create_enabled = True

    @blp.response(PersonSchema(many=True))
    @blp.paginate(CursorPage)
    @combined_search_by(
        Person.first_name, Person.last_name, search_parameter_name="query",
    )
    def get(self):
        return Person.query

    @blp.arguments(PersonSchema)
    @blp.response(PersonSchema)
    def post(self, args: dict) -> Act:
        values = {key: value for key, value in args.items() if value is not None}
        return super().post(values)


@blp.route("/<string:person_id>")
class PersonView(ResourceView):
    model = Person
    decorators = []
    get_enabled = True
    update_enabled = True
    delete_enabled = True

    def _lookup(self, person_id: str) -> Act:
        act = self.model.query.filter_by(extid=person_id).one_or_none()
        if not act:
            abort(404)
        return act

    @blp.response(PersonSchema)
    def get(self, person_id: str) -> BaseQuery:
        return super().get(person_id)

    @blp.arguments(PersonSchema)
    @blp.response(PersonSchema)
    def patch(self, args: dict, person_id: str) -> BaseQuery:
        values = {key: value for key, value in args.items() if value is not None}
        return super().patch(args=values, pk=person_id)

    @blp.response()
    def delete(self, person_id: str):
        return super().delete(person_id)
