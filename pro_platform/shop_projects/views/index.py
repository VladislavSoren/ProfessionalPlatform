from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from celery.result import AsyncResult
from django.http import HttpResponse, HttpRequest, JsonResponse

from shop_projects.tasks import notify_order_saved


class ShopIndexView(TemplateView):
    template_name = "shop_projects/index.html"


@login_required
def get_task_info(request: HttpRequest, task_id: str) -> HttpResponse:
    task_result: AsyncResult = notify_order_saved.AsyncResult(task_id)

    return JsonResponse({
        "task_id": task_result.id,
        "task_status": task_result.status,
        "name": task_result.name,
    })
