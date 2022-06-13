import json
import requests
from django.shortcuts import redirect
from .models import Tasks, Checklists
from django.views.generic import TemplateView, RedirectView
from django.http import Http404

class home(TemplateView):
    template_name="html/home.html"

    def get_context_data(self):
        context = super().get_context_data()
        tasks = requests.get("http://127.0.0.1:8000/api/task/")
        css_progress_list=[]
        str_progress_list=[]
        context["tasks"] = json.loads(tasks.text)
        for task in context["tasks"]:
            try:
                task["deadline"]=replace(task, "deadline")
                dummy={}
                dummy["task_progress"] = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={task['uuid']}").text)
                count=0
                percent=0
                for progress_bool in dummy["task_progress"]:
                    if progress_bool["checked"]:
                        percent+=1
                        count+=1
                    else:
                        count+=1
                css_progress_list.append("style="+str("width:"+str(round(((percent*100)/(count)),1))+"%;"))
                str_progress_list.append(str(round((percent*100)/(count)))+" %")
            except:
                css_progress_list.append("style="+str("width:0%;"))
                str_progress_list.append("情報なし")
        context['css_progress_list'] = css_progress_list
        context['str_progress_list'] = str_progress_list

        return context

class detail(TemplateView):
    template_name="html/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        pk=self.kwargs.get("pk")
        context["task"]=json.loads(requests.get(f"http://127.0.0.1:8000/api/task/{pk}").text)
        task=context["task"]
        task["deadline"]=replace(task, "deadline")
        task["created_at"]=replace(task, "created_at")
        task["updated_at"]=replace(task, "updated_at")
        context["checks"]=json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        return context

    def post(self, request, *args, **kwargs):
        pk=str(self.kwargs.get("pk"))
        beforechecks=json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        updatechecks=request.POST.getlist("checkbool")
        
        for beforecheck in beforechecks:
            if beforecheck["uuid"] not in updatechecks:
                beforecheck["checked"]=False
                requests.put(f"http://127.0.0.1:8000/api/checklist/{beforecheck['uuid']}/", data=beforecheck)
            else:
                beforecheck["checked"]=True
                requests.put(f"http://127.0.0.1:8000/api/checklist/{beforecheck['uuid']}/", data=beforecheck)

        url=f"http://127.0.0.1:8000/detail/{pk}"
        return redirect(to=url)

class edit(TemplateView):
    template_name="html/edit.html"
    model=Tasks
    context_object_name="task"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["checks"]=Checklists.objects.filter(parent_task=self.kwargs.get("pk"))
        return context
    
    def post(self, request, *args, **kwargs):
        pk=self.kwargs.get("pk")
        taskupdate = Tasks.objects.get(pk=pk)
        taskupdate.title = request.POST['title']
        taskupdate.discription = request.POST['discription']
        taskupdate.deadline = (request.POST['deadline']).replace("/","-")
        taskupdate.participants = request.POST['participants']
        taskupdate.save()
        beforecheck = Checklists.objects.filter(parent_task=taskupdate)
        checks = request.POST.getlist("checks")
        for before in beforecheck:
            if before.content not in checks:
                before.delete()
        for check in checks:
            if check:
                if Checklists.objects.filter(content=check,parent_task=taskupdate).exists():
                    continue
                else:
                    check_update = Checklists(content=check,checked=False,parent_task=taskupdate)
                    check_update.save()
        url="http://127.0.0.1:8000/detail/"+str(pk)
        return redirect(to=url)

class maketask(TemplateView):
    template_name="html/maketask.html"

    def post(self, request, *args, **kwargs):
        response=requests.post(
            "http://127.0.0.1:8000/api/task/",
            data=
            {
                "title":request.POST['title'],
                "discription":request.POST['discription'],
                "deadline":(request.POST['deadline']).replace("/","-"),
                "participants":request.POST['participants']
            }
        )
        checks = request.POST.getlist("checks")
        for check in checks:
            requests.post(
                "http://127.0.0.1:8000/api/checklist/",
                data=
                {
                    "content":check,
                    "checked":False,
                    "parent_task":response.text[1:-1]
                }
            )
        return rd_home(request)

class redirecthome(RedirectView):
    url="http://127.0.0.1:8000/home/"
rd_home=redirecthome.as_view()

def deletetask(request, pk):
    try:
        requests.delete(f"http://127.0.0.1:8000/api/task/{pk}/")
    except Tasks.DoesNotExist:
        raise Http404("Task does not exist")
    return rd_home(request)

def replace(text,name):
    text[name]=text[name][: text[name].find("-")] + "年" + text[name][text[name].find("-")+1 :]
    text[name]=text[name][: text[name].find("-")] + "月" + text[name][text[name].find("-")+1 :]
    text[name]=text[name][: text[name].find("T")] + "日" + text[name][text[name].find("T")+1 :]
    text[name]=text[name][: text[name].find(":")] + "時" + text[name][text[name].find(":")+1 :]
    text[name]=text[name][: text[name].find(":")] + "分" + text[name][text[name].find(":")+1 :]
    text[name]=text[name][: text[name].find("分")+1]
    return text[name]

# Create your views here.
