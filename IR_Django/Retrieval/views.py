from django.shortcuts import render,redirect
from .forms import SearchForm
from pymongo import MongoClient
import operator
import re

client=MongoClient()
db=client["irproject"]
collection=db["sofusers"]
key_list=list(collection.find({"keys_terms":"keys"}))[0]["k"]


def user_retrieval(tag_list,query):
    client=MongoClient()
    db=client["irproject"]
    collection=db["sofusers"]

    quer=query.split(" ")
    key_terms=tag_list
    
    for q in quer:
        q=q.lower()
        if (q in key_list) and (q not in key_terms):
            key_terms.append(q) 

    print(key_terms)        
    
    key_term_list=['0']*len(key_terms)
    for i in range(len(key_terms)):
        k=key_terms[i]
        key_term_list[i]=list(collection.find({"technology":k}))[0]["users"]

    if(len(key_term_list)==1):
        inter=key_term_list[0]
        union=key_term_list[0]

    else:
        j=0
        for i in range(len(key_term_list)-1):
            if(j==0):
                inter=dict(key_term_list[i].items() & key_term_list[i+1].items())
                j=j+1
            else:
                inter=dict(inter & key_term_list[i+1].items())

        union={}

        j=0
        for i in range(len(key_term_list)-1):
            if(j==0):
                union=dict(key_term_list[i].items() | key_term_list[i+1].items())
                j=j+1
            else:
                union=dict(inter | key_term_list[i+1].items())

        
    users_inter=[]
    users_union=[]

    
    inter_sorted=sorted(inter.items(),key=operator.itemgetter(1))
    j=0
    for val in reversed(inter_sorted):
        users_inter.append(val[0])
        j=j+1
        if(j>6):
            break
        print(val[0]+"::"+str(val[1]))
    

    union_sorted=sorted(union.items(),key=operator.itemgetter(1))
    j=0
    for val in reversed(union_sorted):
        users_union.append(val[0])
        j=j+1
        if(j>6):
            break
        print(val[0]+"::"+str(val[1]))

    if(len(users_inter)>=5):
        return users_inter[:5]
    else:
        if(len(users_inter)!=0):
            users=users_inter+users_union[:(5-len(users_inter))]
        elif(len(users_inter)==0):
            users=users_union[:5]

        return users



# Create your views here.
def home(request):
    result = None
    posted='0'
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        result = search_form.is_valid()
        if search_form.is_valid():
            tags = search_form.cleaned_data['search_tags']
            query = search_form.cleaned_data['search_query']
            clean = re.compile('<.*?>')
            # print(tags)
            tags = re.sub(clean, ',', tags)
            print(tags)
            tags = tags.strip(',')
            # tag = list(set(re.findall(r"[\w']-[\w]+|[,]",tag)))
            tag  = tags.split(',,')
            print(tag)
           # tag.remove(',')
            users=user_retrieval(tag,query)
            posted='1'
                        
    else:
        search_form = SearchForm()

    if(posted=='0'):
        context = {
            'search_form': search_form,
            'result': result,
            'keys': key_list,
            'posted':posted
        }
    elif(posted=='1'):
        context = {
            'search_form': search_form,
            'result': result,
            'keys': key_list,
            'users':users,
            'posted':posted
        }    
    return render(request, 'Retrieval/search.html', context)


  