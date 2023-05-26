from app.getters.universal import transform
from app.models import ReportImage
from app.schemas import GettingReportImage

def get_report_image(report_image: ReportImage) -> GettingReportImage:
    # return transform(db_obj=order, target_schema=GettingOrder, user=get_user(order.user) if order.user is not None else None)
    return transform(db_obj=report, target_schema=GettingReportImage)