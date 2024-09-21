from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Invoice, Entry
import json

def nav_context(index: int):

    pages_list = ['Dashboard', 'Invoices', 'Entries']
    icons_list = ['dashboard', 'payments', 'account_balance']

    context = {
        'page_icon_pairs': zip(pages_list, icons_list),
        'current_page': pages_list[index],
        'current_icon': icons_list[index],
    }

    return context

def dashboard(request):
    current_index = 0
    return render(request, "dashboard.html", nav_context(current_index))


def invoice(request):
    current_index = 1
    model_instances = Invoice.objects.all()

    if len(model_instances) > 0:
        context_invoice = []

        for invoice in model_instances:
            context_dict = {}
            context_due = 0

            context_dict['id'] = 'INV-' + str(invoice.id)
            context_dict['due_date'] = invoice.due_date
            context_dict['customer'] = invoice.customer
            context_dict['status'] = invoice.status

            for item_dict in invoice.items:
                temp_amount = int(item_dict['quantity']) * int(item_dict['unitPrice'])
                temp_amount -= int(item_dict['taxRate'])
                context_due += temp_amount

            context_dict['due'] = context_due
            context_invoice.append(context_dict)
    else:
        context_invoice = []

    context = nav_context(current_index)

    if context_invoice:
        context['invoice_rows'] = context_invoice

    return render(request, 'invoice.html', context)


@csrf_exempt
def create_invoice(request):
    if request.method == "GET":
        current_index = 1

        context = nav_context(current_index)

        context['page_name'] =  'New Invoice'
        context['icon_name'] = 'edit_square'
        context['js_url'] = 'new_invoice.js'

        return render(request, 'create_invoice.html', context)

    else:
        data = json.loads(request.body)

        new_invoice = Invoice.objects.create(
            date = data['date'],
            due_date = data['dueDate'],
            customer = data['customerName'],
            items = data['products'],
            status = 'Pending',
        )

        total_amount = 0
        for item_dict in new_invoice.items:
            temp_amount = int(item_dict['quantity']) * int(item_dict['unitPrice'])
            temp_amount -= int(item_dict['taxRate'])
            total_amount += temp_amount


        Entry.objects.create(
            transaction_id = new_invoice.id,
            start_date = new_invoice.date,
            debit_account_name = new_invoice.customer,
            credit_account_name = 'Sales',
            category = 'Trade Receivable',
            amount = total_amount,
        )

        return JsonResponse({ "message": "Data Recieved Successfully" })


def entries(request):
    current_index = 2
    entries = Entry.objects.all()

    context = nav_context(current_index)
    if len(entries) > 0:
        context['entries'] = entries

    return render(request, 'entries.html', context)