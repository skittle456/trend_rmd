$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});
$(document).ready(function(){
    var ctx = $('#output-chart');
    var data;
    data.append({x:"bussiness",y:"{{ values.0 }}"});
    data.append({x:"entertainment",y:"{{ values.1 }}"});
    data.append({x:"food",y:"{{ values.2 }}"});
    data.append({x:"health",y:"{{ values.3 }}"});
    data.append({x:"music",y:"{{ values.4 }}"});
    data.append({x:"plant",y:"{{ values.5 }}"});
    data.append({x:"politics",y:"{{ values.6 }}"});
    data.append({x:"sport",y:"{{ values.7 }}"});
    data.append({x:"tech",y:"{{ values.8 }}"});
    var outputChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
});
