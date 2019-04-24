create_button = document.getElementById('create_button')


create_button.addEventListener('click', function(){
    $.ajax({
        url: 'data/',
        method: 'GET',
        data:{
            'query': 'select * from event limit 10;'
        },
        dataType: 'json',
        success:function(data){
            if(data['has']){
                console.log(data['data']);
            }
        },
        fail:function(){
            console.log("cannot send code to server");
            }
    });
});

ds = []
for(var i = 0; i < 100; i++){
    ds.push({
        label: 'Scatter Dataset',
        backgroundColor: "rgba(246,156,85,1)",
        borderColor: "rgba(246,156,85,1)",
        fill: false,
        borderWidth : 15,
        pointRadius : 0,
        data: [
            {
                x: i,
                y: i
            }, {
                x: i+2,
                y: i
            }
        ]
    })
}


var ctx = document.getElementById('myChart').getContext('2d');
ctx.width = 400;
ctx.height = 400;
var scatterChart = new Chart(ctx, {
type: 'line',
data: {
    datasets: ds
},
options: {
    legend : {
        display : false
    },
    scales: {
        xAxes: [{
            type: 'linear',
            position: 'bottom',
            ticks : {
                beginAtzero :true,
                stepSize : 1
            }
        }],
        yAxes : [{
            scaleLabel : {
                display : true
            },
            ticks : {
                beginAtZero :true,
                max : 100
            }
        }]
    }
}
});
