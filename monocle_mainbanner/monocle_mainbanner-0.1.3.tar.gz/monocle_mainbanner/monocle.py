appname = 'monocle_mainbanner'
context_callback =  "'monocle_mainbanner_models': MainBanner.objects.all().filter(isShown=True)"
models = ['MainBanner']
included_app_reqs = [
]