import json
import requests
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Tasks, Checklists
from django.views.generic import ListView, DetailView, TemplateView, RedirectView
from django.http import Http404

class home(TemplateView):
    template_name="html/home.html"

    def get_context_data(self):
        context = super().get_context_data()
        tasks = requests.get("http://127.0.0.1:8000/api/task?format=json")
        css_progress_list=[]
        str_progress_list=[]
        context["tasks"] = json.loads(tasks.text)
        for task in context["tasks"]:
            try:
                task["deadline"]=task["deadline"][: task["deadline"].find("-")] + "年" + task["deadline"][task["deadline"].find("-")+1 :]
                task["deadline"]=task["deadline"][: task["deadline"].find("-")] + "月" + task["deadline"][task["deadline"].find("-")+1 :]
                task["deadline"]=task["deadline"][: task["deadline"].find("T")] + "日" + task["deadline"][task["deadline"].find("T")+1 :]
                task["deadline"]=task["deadline"][: task["deadline"].find(":")] + "時" + task["deadline"][task["deadline"].find(":")+1 :]
                task["deadline"]=task["deadline"][: task["deadline"].find(":")] + "分" + task["deadline"][task["deadline"].find(":")+1 :]
                task["deadline"]=task["deadline"][: task["deadline"].find("分")+1]
                dummy={}
                dummy["task_progress"] = json.loads(requests.get(("http://127.0.0.1:8000/api/checklist/?parent_task="+task['uuid'])+"?format=json").text)
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

class detail(DetailView):
    template_name="html/detail.html"
    model=Tasks
    context_object_name="task"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["checks"]=Checklists.objects.filter(parent_task=self.kwargs.get("pk"))
        return context

    def post(self,request,*args,**kwargs):
        checks = Checklists.objects.filter(parent_task=self.kwargs.get("pk"))
        latestchecks=request.POST.getlist("checkbool")

        beforecheck=[]
        for check_before_bool in checks:
            beforecheck.append(str(check_before_bool.pk))

        updatechecks=[]
        for check_after_bool in latestchecks:
            updatechecks.append(str(check_after_bool))
        
        for b_check in beforecheck:
            change_check=Checklists.objects.get(pk=b_check)
            if b_check not in updatechecks:
                change_check.checked=0
            else:
                change_check.checked=1
            change_check.save()

        url="http://127.0.0.1:8000/detail/"+str(self.kwargs.get("pk"))
        return redirect(to=url)

class edit(DetailView):
    template_name="html/edit.html"
    model=Tasks
    context_object_name="task"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context["checks"]=Checklists.objects.filter(parent_task=self.kwargs.get("pk"))
        return context
    
    def post(self,request,*args,**kwargs):
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
            Tasks.objects.create(title=request.POST['title'], discription=request.POST['discription'], deadline=(request.POST['deadline']).replace("/","-"), participants=request.POST['participants'])
            checks = request.POST.getlist("checks")
            for check in checks:
                if check:
                    if Checklists.objects.filter(content=check,parent_task=Tasks.objects.order_by('-created_at')[0]).exists():
                        continue
                    else:
                        Checklists.objects.create(content=check,checked=False,parent_task=Tasks.objects.order_by('-created_at')[0])
            return rd_home(request)

class redirecthome(RedirectView):
    url="http://127.0.0.1:8000/home/"
rd_home=redirecthome.as_view()

def deletetask(request, task_pk):
    try:
        task = Tasks.objects.get(pk=task_pk)
    except Tasks.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return rd_home(request)

# Create your views here.
