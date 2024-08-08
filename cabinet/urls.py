from django.template.defaulttags import url
from django.urls import path

import cabinet.views

urlpatterns = [
    path("statistic/<str:flat_id>", cabinet.views.Statistic.as_view(), name='flat_statistic_cabinet'),

    path("receipts", cabinet.views.ReceiptList.as_view(), name='receipts_cabinet'),
    path("invoice", cabinet.views.Invoice.as_view(), name='invoice'),
    path("receipt_to_pdf_print/<str:receipt_id>", cabinet.views.ReceiptPDF.as_view(), name='receipt_to_pdf_print'),
    path("receipt_to_pdf2/<str:receipt_id>", cabinet.views.ReceiptPDF2.as_view(), name='receipt_to_pdf2'),
    path("flat_receipts/<str:flat_id>", cabinet.views.FlatReceiptList.as_view(), name='get_flat_receipts_cabinet'),
    path("filtered_receipts", cabinet.views.ReceiptsFilteredList.as_view(),
         name='filtered_receipts_cabinet'),
    path("flat_filtered_receipts/<str:flat_id>", cabinet.views.FlatReceiptsFilteredList.as_view(),
         name='flat_filtered_receipts_cabinet'),
    path("receipt/detail/<str:pk>", cabinet.views.ReceiptDetail.as_view(), name='read_receipt_cabinet'),


    path("tariff/detail/<str:flat_id>", cabinet.views.TariffDetail.as_view(), name='get_tariff_cabinet'),


    path("mailbox", cabinet.views.MailboxList.as_view(), name='mailboxes_cabinet'),
    path("filtered_messages", cabinet.views.MailboxFilteredList.as_view(),
         name='filtered_messages_cabinet'),
    path("mailbox/detail/<str:pk>", cabinet.views.MailboxDetail.as_view(), name='mailbox_detail_cabinet'),
    path("mailbox/delete/<str:pk>", cabinet.views.DeleteMailbox.as_view(),
         name='delete_mailbox_cabinet'),


    path("applications", cabinet.views.ApplicationList.as_view(), name='applications_cabinet'),
    path("application/add", cabinet.views.CreateApplication.as_view(), name='add_application_cabinet'),


    path("profile", cabinet.views.Profile.as_view(), name='profile'),
    path("profile/update/<str:pk>", cabinet.views.UpdateProfileView.as_view(), name='update_profile'),

]
