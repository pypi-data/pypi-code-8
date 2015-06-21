'''
Created on Mar 4, 2015

@author: winston
'''
from selenium import webdriver

js = '''
var url = "http://www.ankangwang.com/shuxiang/yang/66193.html";

var server_url = 'http://192.168.33.190:8000/article/upload';

var results = {
    'url' : url,
};

function open_target(callback) {
         var page = require('webpage').create();
        page.open(url, function(status) {
            if (status === "success") {
                console.log(page.injectJs("jquery-1.10.2_d88366fd.js") ? "... done injecting jquery!" : "... failed to inject jquery!");
                results['html'] = page.evaluate(function() {
                    var width = $(document).width();
                    var height = $(document).height();
                    $('body').attr('__atr_width', width);
                    $('body').attr('__atr_height', height);
                    var the_id = 0;
                    $('body').remove('script').find('*').not('script, style, noscript, iframe').each(function() {
                        if (this.tagName.indexOf(':') < 0) {
                            var $this = $(this);
                            var pos = $this.offset();
                            $this.attr('__atr_id', the_id++);
                            $this.attr('__atr_width', $this.width());
                            $this.attr('__atr_height', $this.height());
                            $this.attr('__atr_top', pos['top']);
                            $this.attr('__atr_left', pos['left']);
                            $this.attr('__atr_visible', $this.is(":visible"));
                            $this.attr('__atr_font-size', $this.css('font-size'));
                            $this.attr('__atr_text-align', $this.css('text-align'));
                        }
                    });
                    // return $('body').attr('__atr_height');
                    return document.all[0].outerHTML;
                });
                console.log('teststssss');
                console.log(results['html'].length);
                    
            }
            page.close();
            callback.apply();
        });
}

function upload_results() {
    console.log('aaa');
    var upload_page = require('webpage').create();
    
    
    var data = [
        'url=',
        encodeURIComponent(results['url']),
        '&html=',
        encodeURIComponent(results['html']),
    ].join('');    
    
    console.log('here--------------------');
    console.log(results['html'].length);
    upload_page.open(server_url, 'post', data, function(status) {
        if (status !== 'success') {
            console.log(page);
            console.log(server_url);
            console.log(status);
        } else {
            console.log("Post successed!");
            console.log(upload_page.content);
        }
        phantom.exit();
    }); 
}

open_target(upload_results);

'''

if __name__ == '__main__':
    driver = webdriver.PhantomJS()
    driver.execute_script(js)
    driver.quit()