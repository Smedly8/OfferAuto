from app.getters.universal import transform
from app.models import Report
from app.schemas import GettingReport

def get_report(report: Report) -> GettingReport:
    # return transform(db_obj=order, target_schema=GettingOrder, user=get_user(order.user) if order.user is not None else None)
    return transform(db_obj=report, target_schema=GettingReport)