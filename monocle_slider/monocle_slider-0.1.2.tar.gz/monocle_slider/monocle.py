appname = 'monocle_slider'
context_callback =  "'monocle_slide_models': Slide.objects.all(), 'monocle_slider_models': Slider.objects.all().filter(isShown=True)"
models = ['Slider', 'Slide']
included_app_reqs = [
]