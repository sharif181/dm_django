from django.shortcuts import render
from django.http import HttpResponse
import pickle
import pandas as pd
from dmapp.models import CustomerInfo
import randominfo


def HomeView(request):
    return render(request, 'home-page.html')


def customerList(request):
    if request.POST:
        params = get_params(request.POST.get('product'), request.POST.get('level'))
        user_ids = get_user_ids(params)
        customers = CustomerInfo.objects.filter(user_id__in=user_ids)
        exportData(customers)
        context = {
            "download_link": '/media/export.csv',
            "customers": customers
        }
        return render(request, 'customer-list.html', context)
    else:
        return HttpResponse("Get request not allowed")


def get_params(product, level):
    model_path = './dm_files/final_model.pkl'
    data_mining_model = pickle.load(open(model_path, 'rb'))
    target = '{\'%s_segment_%s\'}' % (product, level)
    results_personnal_care = data_mining_model[
        data_mining_model['consequents'].astype(str).str.contains(target, na=False)].sort_values(by='confidence',
                                                                                                 ascending=False)
    items = results_personnal_care.iloc[0][0]
    queries = []
    col_names = []
    for item in items:
        splited_item = item.split('_')
        queries.append(splited_item[-1])
        col_names.append('_'.join(splited_item[0:-1]))

    return {"col_names": col_names, "queries": queries}


def get_user_ids(params):
    file_path = './dm_files/final_file.csv'
    data = pd.read_csv(file_path, sep=',')
    col_names = params.get('col_names')
    queries = params.get('queries')
    for col, que in zip(col_names, queries):
        data = data[data[col] == que]
    return data['ID'].tolist()


def importData():
    file_path = './dm_files/marketing_campaign.csv'
    data = pd.read_csv(file_path, sep='\t')
    user_ids = data['ID'].tolist()

    for user_id in user_ids:
        number = randominfo.get_phone_number()
        name = randominfo.get_full_name()
        last_name = name.split(' ')[-1]
        email = f'{last_name}@gmail.com'
        customer = CustomerInfo.objects.create(user_id=user_id, name=name, contact_number=number, email=email)
        customer.save()


def exportData(customers):
    user_ids = []
    names = []
    contact_numbers = []
    emails = []
    for custmer in customers:
        user_ids.append(custmer.user_id)
        names.append(custmer.name)
        contact_numbers.append(custmer.contact_number)
        emails.append(custmer.email)

    df = pd.DataFrame({
        "User ID": user_ids,
        "Name": names,
        "Contact Number": contact_numbers,
        "Email": emails
    })
    file_path = './media/export.csv'
    df.to_csv(file_path, sep=',', index=False)

