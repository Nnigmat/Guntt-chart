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
                console.log(data['data'][3][0]['task_name']);
            }
        },
        fail:function(){
            console.log("cannot send code to server");
            }
    });
});
