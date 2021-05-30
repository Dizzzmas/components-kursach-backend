from flask_smorest import Blueprint
from jetkit.api import CursorPage, combined_search_by, searchable_by
from smorest_crud import CollectionView

from db_kursach_s2.api.act.schema import ActSchema
from db_kursach_s2.model import Act, Person

blp = Blueprint("Act", __name__, url_prefix="act")


@blp.route("")
class ActCollection(CollectionView):
    model = Act

    list_enabled = True
    create_enabled = True

    @blp.response(ActSchema(many=True))
    @blp.paginate(CursorPage)
    @combined_search_by(
        Person.first_name, Person.last_name, search_parameter_name="query",
    )
    @searchable_by(Act.type, search_parameter_name="type", exact_match=True)
    def get(self):
        return Act.query.join(Person, isouter=True)

    # @blp.arguments(DeveloperSchema)
    # @blp.response(DeveloperSchema)
    # def post(self, args: dict) -> Developer:
    #     args.update(owner=get_current_user())
    #     return super().post(args)
