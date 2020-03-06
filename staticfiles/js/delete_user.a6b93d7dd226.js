function delete_user(){
    // dummy data
    info = {
        'action':'delete',
        'user_id':'4',
        'uuid':'c4971e44-a4d8-4675-ad27-e7b3fd24332a',
    }
    $.ajax (
        {
            type: 'POST',
            url: '/user/modify',
            data: JSON.stringify(info),
            success: function(data){
                console.log(data)
                if(data['status']){
                }                
            },
            error: function(data){ 
                console.log(data)
            }
        });
}

function revive_user(){
    // dummy data
    info = {
        'action':'revive',
        'user_id':'4',
        'uuid':'c4971e44-a4d8-4675-ad27-e7b3fd24332a',
    }
    $.ajax (
        {
            type: 'POST',
            url: '/user/modify',
            data: JSON.stringify(info),
            success: function(data){
                console.log(data)
                if(data['status']){
                }                
            },
            error: function(data){ 
                console.log(data)
            }
        });
}
