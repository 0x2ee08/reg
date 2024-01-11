google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);
var url_link = location.protocol+"//"+location.hostname+"/api/"


function drawChart(time) {
    let x = document.cookie;
    x = x.split('=');
    var token = x[1];

    let gmail;

    const info = {
        "token": token
    }

    const options = {
        method: 'POST',
        body: JSON.stringify(info)
    };

    //change url here
    fetch(url_link + 'get_all_info', options).then(res => res.json()).then(data => {
        console.log(data)
        var my_day = document.getElementById("my_day").innerHTML;
        my_day = my_day.split(" ");
        my_day = my_day[3];
        my_day = my_day.split("-");
        day = my_day[0];
        month = my_day[1];
        year = my_day[2];
        //console.log(day,month,year);

        var matrix = [['Ngày', 'Thân nhiệt', 'Nhiệt độ cao']];
        var arr = []
        var mem = 37;


        for (let info in data) {
            console.log(info)
            if (info != "lopHocSinh" && info != "tenHocSinh" && info != 'gmailHocSinh' && info != "_id") {
                if(data[info]['thanNhiet'] != undefined || data[info['thanNhiet']!= null]){
                    arr.push(info)
                    arr.push(parseFloat(data[info]['thanNhiet']))
                }
                else {
                    arr.push(info + " Không đo")
                    arr.push(0)
                }
                arr.push(37.5)
                matrix.push(arr)
                arr = []
            }
        }


        var data = google.visualization.arrayToDataTable(matrix);


        var options = {
            title: 'Bảng thông kê nhiệt độ học sinh',
            curveType: 'function',
            legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
    });
}