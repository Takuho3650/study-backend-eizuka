import json
import requests
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView

class home(TemplateView):
    template_name = "html/home.html"

    def get_context_data(self):
        context = super().get_context_data()
        tasks = requests.get("http://127.0.0.1:8000/api/task/")
        css_progress_list = []
        str_progress_list = []
        context["tasks"] = json.loads(tasks.text)
        for task in context["tasks"]:
            try:
                task["deadline"] = replace(task, "deadline")
                dummy = {}
                dummy["task_progress"] = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={task['uuid']}").text)
                count = 0
                percent = 0
                for progress_bool in dummy["task_progress"]:
                    if progress_bool["checked"]:
                        percent += 1
                        count += 1
                    else:
                        count += 1
                css_progress_list.append("style="+str("width:"+str(round(((percent*100)/(count)),1))+"%;"))
                str_progress_list.append(str(round((percent*100)/(count)))+" %")
            except:
                css_progress_list.append("style="+str("width:0%;"))
                str_progress_list.append("情報なし")
        context['css_progress_list'] = css_progress_list
        context['str_progress_list'] = str_progress_list

        return context

class detail(TemplateView):
    template_name = "html/detail.html"

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        context = super().get_context_data()
        context["task"] = json.loads(requests.get(f"http://127.0.0.1:8000/api/task/{pk}/").text)
        task = context["task"]
        task["deadline"] = replace(task, "deadline")
        task["created_at"] = replace(task, "created_at")
        task["updated_at"] = replace(task, "updated_at")
        context["checks"] = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        taskdata = json.loads(requests.get(f"http://127.0.0.1:8000/api/task/{pk}/").text)
        requests.put(f"http://127.0.0.1:8000/api/task/{pk}/", data=taskdata)

        beforechecks = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        updatechecks = request.POST.getlist("checkbool")
        
        for beforecheck in beforechecks:
            if beforecheck["uuid"] not in updatechecks:
                beforecheck["checked"] = False
                requests.put(f"http://127.0.0.1:8000/api/checklist/{beforecheck['uuid']}/", data=beforecheck)
            else:
                beforecheck["checked"] = True
                requests.put(f"http://127.0.0.1:8000/api/checklist/{beforecheck['uuid']}/", data=beforecheck)

        url = f"http://127.0.0.1:8000/detail/{pk}/"
        return redirect(to=url)

class edit(TemplateView):
    template_name = "html/edit.html"

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        context = super().get_context_data()
        context["task"] = json.loads(requests.get(f"http://127.0.0.1:8000/api/task/{pk}/").text)
        context["checks"] = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        requests.put(
            f"http://127.0.0.1:8000/api/task/{pk}/",
            data =
            {
                "uuid":pk,
                "title":request.POST['title'],
                "discription":request.POST['discription'],
                "deadline":(request.POST['deadline']).replace("/", "-"),
                "participants":request.POST['participants']
            }
        )
        
        beforecheck = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        lst = request.POST.getlist("checks")
        checks = (sorted(set(lst), key=lst.index))
        for before in beforecheck:
            if before["content"] not in checks:
                requests.delete(f"http://127.0.0.1:8000/api/checklist/{before['uuid']}/")

        beforecheck_deleted = json.loads(requests.get(f"http://127.0.0.1:8000/api/checklist/?parent_task={pk}").text)
        for before_deleted in beforecheck_deleted:
            if before_deleted["content"] in checks:
                checks.remove(before_deleted["content"])

        for check in checks:
            requests.post(
                    "http://127.0.0.1:8000/api/checklist/",
                    data =
                    {
                        "content":check,
                        "checked":False,
                        "parent_task":pk,
                    }
            )
                
        url = f"http://127.0.0.1:8000/detail/{pk}/"
        return redirect(to=url)

class maketask(TemplateView):
    template_name = "html/maketask.html"

    def post(self, request, *args, **kwargs):
        response = requests.post(
            "http://127.0.0.1:8000/api/task/",
            data =
            {
                "title":request.POST['title'],
                "discription":request.POST['discription'],
                "deadline":(request.POST['deadline']).replace("/", "-"),
                "participants":request.POST['participants']
            }
        )
        lst = request.POST.getlist("checks")
        checks = (sorted(set(lst), key=lst.index))
        for check in checks:
            requests.post(
                "http://127.0.0.1:8000/api/checklist/",
                data =
                {
                    "content":check,
                    "checked":False,
                    "parent_task":response.text[1:-1]
                }
            )
        return rd_home(request)

class redirecthome(RedirectView):
    url = "http://127.0.0.1:8000/home/"
rd_home = redirecthome.as_view()

def deletetask(request, pk):
    requests.delete(f"http://127.0.0.1:8000/api/task/{pk}/")
    return rd_home(request)

def replace(text, name):
    text[name] = text[name][: text[name].find("-")] + "年" + text[name][text[name].find("-") + 1 :]
    text[name] = text[name][: text[name].find("-")] + "月" + text[name][text[name].find("-") + 1 :]
    text[name] = text[name][: text[name].find("T")] + "日" + text[name][text[name].find("T") + 1 :]
    text[name] = text[name][: text[name].find(":")] + "時" + text[name][text[name].find(":") + 1 :]
    text[name] = text[name][: text[name].find(":")] + "分" + text[name][text[name].find(":") + 1 :]
    text[name] = text[name][: text[name].find("分")+1]
    return text[name]