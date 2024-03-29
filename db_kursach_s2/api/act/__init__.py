from sqlalchemy import or_

from flask_smorest import Blueprint, abort
from jetkit.api import CursorPage, combined_search_by, searchable_by, sortable_by
from smorest_crud import CollectionView, ResourceView

from db_kursach_s2.api.act.schema import ActSchema, UpsertActSchema
from db_kursach_s2.db import BaseQuery
from db_kursach_s2.model import Act, Person, BirthAct, DeathAct, MarriageAct

blp = Blueprint("Act", __name__, url_prefix="/api/acts")


@blp.route("")
class ActCollection(CollectionView):
    model = Act
    decorators = []
    list_enabled = True
    create_enabled = True

    @blp.response(ActSchema(many=True))
    @blp.paginate(CursorPage, page_size=30)
    @combined_search_by(
        Person.first_name,
        Person.last_name,
        search_parameter_name="query",
    )
    @searchable_by(Act.type, search_parameter_name="type", exact_match=True)
    @sortable_by(Act.created_at)
    def get(self):
        join_conditions = [Person.id == BirthAct.father_id, Person.id == BirthAct.child_id, Person.id == BirthAct.mother_id, Person.id == DeathAct.deceased_id, Person.id == MarriageAct.groom_id, Person.id == MarriageAct.bride_id]
        return Act.query.join(Person, or_(*join_conditions))

    @blp.arguments(UpsertActSchema)
    @blp.response(ActSchema)
    def post(self, args: dict) -> Act:
        values = {key: value for key, value in args.items() if value is not None}
        return super().post(values)


@blp.route("/<string:act_id>")
class ActView(ResourceView):
    model = Act
    decorators = []
    get_enabled = True
    update_enabled = True
    delete_enabled = True

    def _lookup(self, act_id: str) -> Act:
        act = self.model.query.filter_by(extid=act_id).one_or_none()
        if not act:
            abort(404)
        return act

    @blp.response(ActSchema)
    def get(self, act_id: str) -> BaseQuery:
        return super().get(act_id)

    @blp.arguments(UpsertActSchema)
    @blp.response(ActSchema)
    def patch(self, args: dict, act_id: str) -> BaseQuery:
        values = {key: value for key, value in args.items() if value is not None}
        return super().patch(args=values, pk=act_id)

    @blp.response()
    def delete(self, act_id: str):
        return super().delete(act_id)
