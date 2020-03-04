function get_purchase_orders(){
    // dummy data
    info = {
        'filter':'none',
        'action':'get',
        'start':0,
        'end':5
    }
    $.ajax (
        {
            type: 'POST',
            url: '/apiv1/inventory/porders',
            data: JSON.stringify(info),
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}

function get_purchase_order(){
    id = 1;
    $.ajax (
        {
            type: 'GET',
            url: '/apiv1/inventory/porders/'+id,
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}