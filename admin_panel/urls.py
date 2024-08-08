from django.urls import path

import admin_panel.views

urlpatterns = [
    path("statistic", admin_panel.views.Statistic.as_view(), name='statistic'),


    path("paybox", admin_panel.views.PayboxList.as_view(), name='paybox'),
    path("filtered_paybox", admin_panel.views.PayboxFilteredList.as_view(),
         name='filtered_paybox'),
    path("paybox/add/<str:income>", admin_panel.views.CreatePaybox.as_view(), name='add_paybox'),
    path("paybox/update/<str:pk>", admin_panel.views.UpdatePaybox.as_view(), name='update_paybox'),
    path("paybox/copy/<str:pk>", admin_panel.views.CopyPaybox.as_view(), name='copy_paybox'),
    path("paybox/detail/<str:pk>", admin_panel.views.PayboxDetail.as_view(), name='read_paybox'),
    path("paybox/delete/<str:pk>", admin_panel.views.DeletePaybox.as_view(), name='delete_paybox'),


    path("receipts", admin_panel.views.ReceiptList.as_view(), name='receipts'),
    path("filtered_receipts", admin_panel.views.ReceiptsFilteredList.as_view(),
         name='filtered_receipts'),
    path("receipt/add", admin_panel.views.CreateReceipt.as_view(), name='add_receipt'),
    path("receipt/update/<str:pk>", admin_panel.views.UpdateReceipt.as_view(), name='update_receipt'),
    path("receipt/copy/<str:pk>", admin_panel.views.CopyReceipt.as_view(), name='copy_receipt'),
    path("receipt/detail/<str:pk>", admin_panel.views.ReceiptDetail.as_view(), name='read_receipt'),
    path("receipt/delete/<str:pk>", admin_panel.views.DeleteReceipt.as_view(), name='delete_receipt'),
    path("receipt/print/<str:pk>", admin_panel.views.ReceiptPrint.as_view(), name='receipt_print'),
    path("receipt/download_excel/<str:excel_id>/<str:receipt_id>", admin_panel.views.ReceiptDownloadExcel.as_view(), name='receipt_download'),
    path("receipt/print_settings", admin_panel.views.ReceiptPrintingSettings.as_view(), name='receipt_print_settings'),
    path("receipt/print_settings/delete/<str:pk>", admin_panel.views.ReceiptPrintingSettingsDelete.as_view(), name='receipt_print_settings_delete'),
    path("receipt/print_settings/default/<str:pk>", admin_panel.views.ReceiptPrintingSettingsDefault.as_view(), name='receipt_print_settings_default'),
    path("send_receipt_email/<str:receipt_id>", admin_panel.views.SendReceiptEmail.as_view(), name='send_receipt_email'),

    path("personal_accounts", admin_panel.views.PersonalAccountListView.as_view(), name='personal_accounts'),
    path("filtered_personal_accounts", admin_panel.views.PersonalAccountFilteredList.as_view(), name='filtered_personal_accounts'),
    path("personal_accounts/add", admin_panel.views.CreatePersonalAccount.as_view(), name='add_personal_account'),
    path("personal_accounts/update/<str:pk>", admin_panel.views.UpdatePersonalAccount.as_view(), name='update_personal_account'),
    path("personal_accounts/detail/<str:pk>", admin_panel.views.PersonalAccountDetail.as_view(), name='read_personal_account'),
    path("personal_accounts/delete/<str:pk>", admin_panel.views.DeletePersonalAccount.as_view(), name='delete_personal_account'),
    path("personal_account_accept_payment/<str:pk>", admin_panel.views.PersonalAccountAcceptPayment.as_view(), name='personal_account_accept_payment'),
    path("personal_account_accept_receipt/<str:pk>", admin_panel.views.PersonalAccountAcceptReceipt.as_view(), name='personal_account_accept_receipt'),
    path("personal_account_receipts/<str:pk>", admin_panel.views.PersonalAccountReceiptList.as_view(), name='personal_account_receipts'),
    path("personal_account_paybox/<str:pk>", admin_panel.views.PersonalAccountPayboxList.as_view(), name='personal_account_paybox'),


    path("flats", admin_panel.views.FlatListView.as_view(), name='flats'),
    path("filtered_flats", admin_panel.views.FlatFilteredList.as_view(),
         name='filtered_flats'),
    path("flats/add", admin_panel.views.CreateFlatView.as_view(), name='add_flat'),
    path("flats/update/<str:pk>", admin_panel.views.UpdateFlatView.as_view(), name='update_flat'),
    path("flats/detail/<str:pk>", admin_panel.views.FlatDetail.as_view(), name='read_flat'),
    path("flats/delete/<str:pk>", admin_panel.views.DeleteFlatView.as_view(), name='delete_flat'),
    path("flat_accept_payment/<str:pk>", admin_panel.views.FlatAcceptPayment.as_view(),
         name='flat_accept_payment'),
    path("flat_accept_receipt/<str:pk>", admin_panel.views.FlatAcceptReceipt.as_view(),
         name='flat_accept_receipt'),
    path("flat_receipts/<str:pk>", admin_panel.views.FlatReceiptList.as_view(),
         name='flat_receipts'),
    path("flat_paybox/<str:pk>", admin_panel.views.FlatPayboxList.as_view(),
         name='flat_paybox'),


    path("clients", admin_panel.views.ClientListView.as_view(), name='clients'),
    path("filtered_clients", admin_panel.views.ClientFilteredListView.as_view(), name='filtered_clients'),
    path("clients/add", admin_panel.views.ClientSignUpView.as_view(), name='add_client'),
    path("clients/update/<str:pk>", admin_panel.views.UpdateClientView.as_view(), name='update_client'),
    path("clients/detail/<str:pk>", admin_panel.views.ClientDetail.as_view(), name='read_client'),
    path("clients/delete/<str:pk>", admin_panel.views.DeleteClientView.as_view(), name='delete_client'),
    path("send_invitation", admin_panel.views.SendInvitation.as_view(), name='send_invitation'),


    path("houses", admin_panel.views.HouseListView.as_view(), name='houses'),
    path("filtered_houses", admin_panel.views.HouseFilteredList.as_view(),
         name='filtered_houses'),
    path("houses/add", admin_panel.views.CreateHouseView.as_view(), name='add_house'),
    path("house/update/<str:pk>", admin_panel.views.UpdateHouseView.as_view(), name='update_house'),
    path("house/detail/<str:pk>", admin_panel.views.HouseDetail.as_view(), name='read_house'),
    path("house/delete/<str:pk>", admin_panel.views.DeleteHouseView.as_view(), name='delete_house'),



    path("mailbox", admin_panel.views.MailboxList.as_view(), name='mailboxes'),
    path("filtered_messages", admin_panel.views.MailboxFilteredList.as_view(),
         name='filtered_messages'),
    path("mailbox/add", admin_panel.views.CreateMailbox.as_view(), name='add_mailbox'),
    path("mailbox/add_debtors", admin_panel.views.CreateDebtorsMailbox.as_view(), name='add_debtors_mailbox'),
    path("mailbox/detail/<str:pk>", admin_panel.views.MailboxDetail.as_view(), name='mailbox_detail'),
    path("mailbox/delete/<str:pk>", admin_panel.views.DeleteMailbox.as_view(),
         name='delete_mailbox'),


    path("applications", admin_panel.views.ApplicationList.as_view(), name='applications'),
    path("filtered_applications", admin_panel.views.ApplicationFilteredList.as_view(),
         name='filtered_applications'),
    path("application/add", admin_panel.views.CreateApplication.as_view(), name='add_application'),
    path("application/update/<str:pk>", admin_panel.views.UpdateApplication.as_view(),
         name='update_application'),
    path("application/detail/<str:pk>", admin_panel.views.ApplicationDetail.as_view(), name='read_application'),
    path("application/delete/<str:pk>", admin_panel.views.DeleteApplication.as_view(),
         name='delete_application'),


    path("counters", admin_panel.views.CounterList.as_view(), name='counters'),
    path("filtered_counters", admin_panel.views.CountersFilteredList.as_view(),
         name='filtered_counters'),
    path("counter_indications/<str:flat>/<str:service>", admin_panel.views.CounterIndicationsList.as_view(), name='counter_indications'),
    path("filtered_counter_indications/<str:flat>", admin_panel.views.CounterIndicationsFilteredList.as_view(),
         name='filtered_counter_indications'),
    path("indication/add", admin_panel.views.CreateIndication.as_view(), name='add_indication'),
    path("indication/add_new/<str:flat>/<str:service>", admin_panel.views.CreateNewIndication.as_view(), name='add_new_indication'),
    path("indication/add_to_flat/<str:flat>", admin_panel.views.CreateIndicationForFlat.as_view(), name='add_indication_to_flat'),
    path("indication/update/<str:pk>", admin_panel.views.UpdateIndication.as_view(), name='update_indication'),
    path("indication/detail/<str:pk>", admin_panel.views.IndicationDetail.as_view(), name='read_indication'),
    path("indication/delete/<str:pk>", admin_panel.views.DeleteIndication.as_view(), name='delete_indication'),
    path("flat_indications/<str:flat>", admin_panel.views.FlatIndicationsList.as_view(), name='flat_indications'),

    path("system_services", admin_panel.views.ServicesView.as_view(), name='system_services'),
    path("system_tariffs", admin_panel.views.TariffsListView.as_view(), name='system_tariffs'),
    path("system_tariffs/add", admin_panel.views.CreateTariffView.as_view(), name='add_tariff'),
    path("system_tariffs/detail/<str:pk>", admin_panel.views.TariffDetail.as_view(), name='tariff_detail'),
    path("system_tariffs/delete/<str:pk>", admin_panel.views.DeleteTariffView.as_view(), name='delete_tariff'),
    path("system_tariffs/update/<str:pk>", admin_panel.views.UpdateTariffView.as_view(), name='update_tariff'),
    path("system_tariffs/copy/<str:pk>", admin_panel.views.CopyTariffView.as_view(), name='copy_tariff'),
    path("system_payment_details", admin_panel.views.UpdatePaymentDetailView.as_view(), name='system_payment_details'),


    path("personals", admin_panel.views.PersonalListView.as_view(),
         name='personals'),
    path("personals_filtered", admin_panel.views.PersonalFilteredList.as_view(),
         name='personals_filtered'),
    path("personals/add", admin_panel.views.PersonalSignUpView.as_view(),
         name='add_personal'),
    path("personals/update/<str:pk>", admin_panel.views.UpdatePersonalView.as_view(),
         name='update_personal'),
    path("personal/detail/<str:pk>", admin_panel.views.PersonalDetail.as_view(), name='read_personal'),

    path("personals/delete/<str:pk>", admin_panel.views.DeletePersonalView.as_view(),
         name='delete_personal'),


    path("system_payment_articles", admin_panel.views.PaymentArticlesListView.as_view(), name='system_payment_articles'),
    path("system_payment_article/add", admin_panel.views.CreatePaymentArticleView.as_view(), name='add_payment_article'),
    path("system_payment_article/update/<str:pk>", admin_panel.views.UpdatePaymentArticleView.as_view(), name='update_payment_article'),
    path("system_payment_article/delete/<str:pk>", admin_panel.views.DeletePaymentArticleView.as_view(), name='delete_payment_article'),


    path("main_page", admin_panel.views.MainPageView.as_view(), name='main_page'),
    path("about_us", admin_panel.views.AboutUsView.as_view(), name='about_us'),
    path("services", admin_panel.views.SiteServicesView.as_view(), name='services'),
    path("tariffs", admin_panel.views.SiteTariffsView.as_view(), name='tariffs'),
    path("contacts", admin_panel.views.ContactsView.as_view(), name='contacts'),


    path("photo/delete/<str:pk>", admin_panel.views.DeletePhotoView.as_view(), name='delete_photo'),
    path("doc/delete/<str:pk>", admin_panel.views.DeleteDocView.as_view(), name='delete_doc'),


    path("get_measure/<str:pk>", admin_panel.views.GetMeasureView.as_view(), name='get_measure'),
    path("get_role/<str:pk>", admin_panel.views.GetRoleView.as_view(), name='get_role'),
    path("get_house-info/<str:pk>", admin_panel.views.GetHouseInfoView.as_view(), name='get_house-info'),
    path("get_flats-for-mailbox/<str:section_id>/<str:floor_id>", admin_panel.views.GetFlatsForMailbox.as_view(), name='get_flat-for-mailbox'),
    path("get_flat_owner-info/<str:pk>", admin_panel.views.GetFlatOwnerInfo.as_view(), name='get_flat_owner-info'),
    path("get_section-info/<str:pk>", admin_panel.views.GetSectionInfoView.as_view(), name='get_section-info'),
    path("get_flat-info/<str:pk>", admin_panel.views.GetFlatInfoView.as_view(), name='get_flat-info'),
    path("get_tariff-info/<str:pk>", admin_panel.views.GetTariffInfoView.as_view(), name='get_tariff-info'),
    path("get_all_flats", admin_panel.views.GetAllFlats.as_view(), name='get_all_flats'),
    path("get_service-info/<str:pk>", admin_panel.views.GetServiceInfoView.as_view(), name='get_service-info'),
    path("get_indication-info/<str:flat_id>/<str:service_id>", admin_panel.views.GetIndicationInfoView.as_view(), name='get_indication-info'),
    path("get_indication-sorted-list/<str:flat_id>", admin_panel.views.GetIndicationsSortedList.as_view(), name='get_indication-sorted-list'),


    path("roles", admin_panel.views.Roles.as_view(), name='roles'),

]
