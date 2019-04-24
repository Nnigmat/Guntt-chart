create_button = document.getElementById('create_button')

create_button.addEventListener('click', function(){
    $.ajax({
        url: 'data/',
        method: 'GET',
        data:{
            'query': 'select * from event order by start_date limit 100'
        },
        dataType: 'json',
        success:function(data){
            if(data['has']){
                var tasks = [];
                for (let value of data['data']) {
                    tasks.push(
                        {
                            id: value[0]['task_name'],
                            name: value[0]['assigned_to'],
                            start: value[0]['start_date'],
                            end: value[0]['end_date'],
                            progress: 100,
                            dependencies: '',
                            custom_class: 'bar-milestone' // optional
                        }
                    )
                }
                var gantt = new Gantt("#gantt", tasks);
                console.log(data)
            }
        },
        fail:function(){
            console.log("cannot send code to server");
            }
    });
});
