from django.contrib import admin
from django.urls import path, include
from main_app.views.action_view import *
from main_app.views.status_view import *
from main_app.views.process_view import *
from main_app.views.department_view import *
from main_app.views.customer_view import *
from main_app.views.view import indexPanelView, logout_view
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", IndexView, name="index"),
    # route for panel/{service}/{id}/{task}
    path(
        "dashboard/",
        include(
            [
                path("order/", include("order.urls")),
                path("", indexPanelView, name="panel"),
                path(
                    "action/",
                    include(
                        [
                            path(
                                "",
                                ActionList,
                                name="action-list",
                            ),
                            path(
                                "add",
                                ActionCreate,
                                name="action-add",
                            ),
                            path(
                                "<pk>/update/",
                                ActionUpdate,
                                name="action-update",
                            ),
                            path(
                                "<pk>/delete/",
                                ActionDelete.as_view(),
                                name="action-delete",
                            ),
                        ]
                    ),
                ),
                path(
                    "status/",
                    include(
                        [
                            path(
                                "",
                                StatusList.as_view(),
                                name="status-list",
                            ),
                            path(
                                "add",
                                StatusCreate,
                                name="status-add",
                            ),
                            path(
                                "<pk>/update/",
                                StatusUpdate,
                                name="status-update",
                            ),
                            path(
                                "<pk>/delete/",
                                StatusDelete.as_view(),
                                name="status-delete",
                            ),
                        ]
                    ),
                ),
                path(
                    "process/",
                    include(
                        [
                            path("", 
                                 ProcessList.as_view(), 
                                 name="process-list"
                                 ),
                            path(
                                "add",
                                ProcessCreate,
                                name="process-add"
                            ),
                            path(
                                "<pk>", 
                                ProcessDetail, 
                                name="process-detail"
                            ),
                            path(
                                "<pk>/update",
                                ProcessUpdate,
                                name="process-update"
                            ),
                            path(
                                "<pk>/delete",
                                ProcessDelete.as_view(),
                                name="process-delete"
                            ),
                        ]
                    ),
                ),
                path(
                    "customer/",
                    include(
                        [
                            path("",
                                 CustomerList,
                                 name="customer-list"
                                 ),
                            path("add/",
                                 CustomerCreate,
                                 name="customer-add"
                                 ),
                            path(
                                "<pk>/update",
                                CustomerUpdate,
                                name="customer-update")  
                        ]
                    ),
                ),
            ],
        ),
        name="dashboard"
    ),
    path("logout/", logout_view, name="logout"),
]
