import os
from webassets import Bundle

CSS_FILES = [
    '/web/css/bq.css',
    '/web/css/bq_ui_toolbar.css',
    '/web/js/bq_ui_misc.css',
    '/web/js/ResourceBrowser/ResourceBrowser.css',
    '/web/js/ResourceTagger/Tagger.css',
    '/web/js/DatasetBrowser/DatasetBrowser.css',
    '/web/js/Share/BQ.share.Dialog.css',
    '/web/js/picker/Path.css',
    '/web/js/tree/files.css',
    '/web/js/tree/organizer.css',
    '/image_service/converter.css',
    '/web/panojs3/styles/panojs.css',
    '/web/js/slider/slider.css',
    '/web/js/picker/Color.css',
    '/web/js/form/field/Color.css',
    '/web/css/imgview.css',
    '/web/js/movie/movie.css',
    '/dataset_service/dataset_panel.css',
    '/web/js/renderers/dataset.css',
    '/web/js/graphviewer/graphviewer.css',
    '/web/js/volume/bioWeb3D.css',
    '/import/bq_ui_upload.css',
    '/export/css/BQ.Export.css',
    '/web/css/bisquik_extjs_fix.css',
    # -- modules
    '/web/js/modules/bq_ui_renderes.css',
]

PRE_JS_FILES = [
    '/web/d3/d3.js',
    '/web/threejs/three.js',
    '/web/threejs/TypedArrayUtils.js',
    '/web/threejs/math/ColorConverter.js',
    '/web/async/async.js',
    '/web/jquery/jquery.min.js',
    '/web/proj4js/proj4.js',
    '/web/raphael/raphael.js',
    ]

JS_FILES = [
    #'/js/bq_ui_extjs_fix.js',
    # --Bisque JsApi - this needs cleaning and updating--
    '/web/js/utils.js',
    '/web/js/bq_api.js',
    '/web/js/bq_ui_application.js',
    '/web/js/bq_ui_toolbar.js',
    '/web/js/bq_ui_misc.js',
    '/web/js/date.js',
    '/web/js/encoder.js',

    # -- ResourceBrowser code --
    '/web/js/ResourceBrowser/Browser.js',
    '/web/js/ResourceBrowser/LayoutFactory.js',
    '/web/js/ResourceBrowser/ResourceQueue.js',
    '/web/js/ResourceBrowser/DatasetManager.js',
    '/web/js/ResourceBrowser/CommandBar.js',
    '/web/js/ResourceBrowser/viewStateManager.js',
    '/web/js/ResourceBrowser/OperationBar.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceFactory.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceImage.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceMex.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceModule.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceDataset.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceFile.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceUser.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceTemplate.js',
    '/web/js/ResourceBrowser/ResourceFactory/ResourceDir.js',
    '/web/js/ResourceBrowser/Misc/MessageBus.js',
    '/web/js/ResourceBrowser/Misc/Slider.js',
    '/web/js/ResourceBrowser/Misc/DataTip.js',

    # -- Gesture manager --
    '/web/js/senchatouch/sencha-touch-gestures.js',
    '/web/js/ResourceBrowser/Misc/GestureManager.js',

    # -- Share dialog files --
    '/web/js/Share/BQ.share.Dialog.js',
    '/web/js/Share/BQ.share.Multi.js',

    # -- ResourceTagger --
    '/web/js/ResourceTagger/ComboBox.js',
    '/web/js/ResourceTagger/RowEditing.js',
    '/web/js/ResourceTagger/Tagger.js',
    '/web/js/ResourceTagger/TaggerOffline.js',
    '/web/js/ResourceTagger/ResourceRenderers/BaseRenderer.js',

    # -- Preferences --
    '/web/js/Preferences/BQ.Preferences.js',
    '/web/js/Preferences/PreferenceViewer.js',
    '/web/js/Preferences/PreferenceTagger.js',
    # -- Admin Page --
    '/web/js/admin/BQ.ModuleManager.js',
    '/web/js/admin/BQ.UserManager.js',
    '/web/js/admin/BQ.AdminPage.js',

    #-- DatasetBrowser --
    '/dataset_service/dataset_service.js',
    '/web/js/DatasetBrowser/DatasetBrowser.js',

    # -- TemplateManager --
    '/web/js/TemplateManager/TemplateTagger.js',
    '/web/js/TemplateManager/TemplateManager.js',
    '/web/js/TemplateManager/TagRenderer.js',

    # -- Tree Organizer --
    '/web/js/picker/Path.js',
    '/web/js/tree/files.js',
    '/web/js/tree/organizer.js',

    # -- PanoJS3 --
    '/web/panojs3/panojs/utils.js',
    '/web/panojs3/panojs/PanoJS.js',
    '/web/panojs3/panojs/controls.js',
    '/web/panojs3/panojs/pyramid_Bisque.js',
    '/web/panojs3/panojs/control_thumbnail.js',
    '/web/panojs3/panojs/control_info.js',
    '/web/panojs3/panojs/control_svg.js',

    # -- Image Service --
    '/image_service/converter.js',
    '/image_service/bq_is_formats.js',

    '/web/js/slider/inversible.js',
    '/web/js/slider/slider.js',
    '/web/js/slider/tslider.js',
    '/web/js/slider/zslider.js',

    '/web/js/picker/Color.js',
    '/web/js/form/field/Color.js',

    '/web/js/viewer/kinetic-v5.1.0.js',

    '/web/js/viewer/scalebar.js',
    '/web/js/viewer/2D.js',
    '/web/js/viewer/imgview.js',
    '/web/js/viewer/imgops.js',
    '/web/js/viewer/imgslicer.js',
    '/web/js/viewer/imgstats.js',
    '/web/js/viewer/listner_zoom.js',
    '/web/js/viewer/tilerender.js',

    '/web/js/viewer/svgrender.js',
    '/web/js/viewer/canvasshapes.js',
    '/web/js/viewer/canvasrender.js',
    '/web/js/viewer/imgedit.js',
    '/web/js/viewer/imgmovie.js',
    '/web/js/viewer/imageconverter.js',
    '/web/js/viewer/imgexternal.js',
    '/web/js/viewer/imgscalebar.js',
    '/web/js/viewer/imginfobar.js',
    '/web/js/viewer/progressbar.js',
    '/web/js/viewer/widget_extjs.js',
    '/web/js/viewer/imgpixelcounter.js',
    '/web/js/viewer/imgcurrentview.js',
    '/web/js/viewer/imgcalibration.js',


    #-- Movie player --
    '/web/js/movie/movie.js',

    #-- Stats --
    '/stats/js/stats.js',
    '/web/js/bq_ui_progress.js',

    #-- GMaps API --
    '/web/js/map/map.js',

    #-- Resource dispatch --
    '/dataset_service/dataset_service.js',
    '/dataset_service/dataset_operations.js',
    '/dataset_service/dataset_panel.js',
    '/web/js/renderers/dataset.js',
    '/web/js/resourceview.js',

    # -- Import Service --
    '/import/File.js',
    '/import/bq_file_upload.js',
    '/import/bq_ui_upload.js',

    # -- Export Service --
    '/export/js/BQ.Export.js',

    # -- Request Animation Frame --
    '/web/js/requestAnimationFrame.js',

    # -- Graph viewer --
    '/web/js/d3Component.js',
    '/web/js/graphviewer/dagre-d3.js',
    '/web/js/graphviewer/GraphViewer.js',

    # -- WebGL viewer --
    '/web/js/volume/lib/whammy.js',
    '/web/js/volume/lib/polygon.js',
    '/web/js/volume/threejs/AnaglyphEffect.js',
    '/web/js/volume/threejs/RotationControls.js',
    '/web/js/volume/threejs/OrbitControls.js',
    '/web/js/volume/threejs/TrackballControls.js',
    '/web/js/volume/volumeConfig.js',
    '/web/js/volume/renderingControls.js',
    '/web/js/volume/lightingControls.js',
    '/web/js/volume/animationControls.js',
    '/web/js/volume/extThreeJS.js',
    '/web/js/volume/gobjectbuffers.js',
    '/web/js/picker/Excolor.js',
    '/web/js/volume/transferEditorD3.js',
    '/web/js/volume/scalebar.js',
    '/web/js/volume/bioWeb3D.js',
    '/web/js/volume/lightingControls.js',

    # -- Modules --
    '/web/js/modules/bq_grid_panel.js',
    '/web/js/modules/bq_ui_renderes.js',

#    '/plugins/**/*.js',
]



def check_files(files):
    for f in files:
        if not os.path.exists ('public%s' %f):
            print "%s is unavailable " % f

    return [ 'public%s' %x  for x in files if os.path.exists ('public%s' %x) ]

all_css = Bundle (
    *check_files (CSS_FILES),
    output = "public/all_css.css"
    )


pre_js = Bundle (
    *check_files (PRE_JS_FILES),
    output='public/pre_js.js'
    )

all_js = Bundle (
    *check_files (JS_FILES),
    output='public/all_js.js'
      )


