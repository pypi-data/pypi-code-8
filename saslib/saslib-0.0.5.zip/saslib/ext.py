import math

def convertSize(size):
    size /= 1024
    size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    if (s > 0):
       return '%s %s' % (s,size_name[i])
    return '0B'

    
template_string = """<!DOCTYPE html>
<html>
<head>
	<script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css" />
    <script>
        $(document).ready(function() {
            $('.display').dataTable();
        } );
    {% for k, v in data.iteritems() %}
        $(document).ready(function () {
            $("#{{k}}_button").click(function () {
                $("#{{k}}_data").slideToggle(300, function () {
                    if ($("#{{k}}_button").val() == "close") {
                        $("#{{k}}_button").val("show detail");
                    } else {
                        $("#{{k}}_button").val("close");
                    }
                });
            });
        });
    {% endfor %}
    </script>
</head>
<body>
<h1> {{ directory }} </h1>
<hr>
{% for k, v in data.iteritems() %}
    <div>
        <header> <h3> {{k}}.sas7bdat </h3> <input id="{{k}}_button" type="button" value="Show detail" /></header>
    </div>
    <div id = "{{k}}_data" style='display:none'>
        <table cellspacing="0" width="100%" >
            {% for key, value in v['detail'].iteritems() %}
                <tr>
                    <th> {{ key }} </th>
                    <td> {{ value }} </td>
                </tr>
            {% endfor %}
        </table>
    </div>

    <table class="display" cellspacing="0" width="100%">
        <thead>
            <tr>
            {% for x in v['meta'][0] %}
                <th> {{ x }} </th>
            {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in v['meta'][1:] %}
            <tr>
                {% for x in row %}
                <td> {{ x }} </td> {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
<hr>
{% endfor %}
</body>
</html>
"""