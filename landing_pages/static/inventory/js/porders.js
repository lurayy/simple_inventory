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
            url: '/apiv1/inventory/porders/'+1,
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}


function get_vendors(){
    info = 
    {
        'action':"get",
        'start':0,
        'end':10
    } 
    $.ajax (
        {
            type: 'POST',
            url: '/apiv1/inventory/vendors',
            data: JSON.stringify(info),
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}


function get_vendor(){
    id = 1
    $.ajax (
        {
            type: 'GET',
            url: '/apiv1/inventory/vendors/'+id,
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}




function get_items(){
    info = 
    {
        'action':"get",
        'start':0,
        'end':10
    } 
    $.ajax (
        {
            type: 'POST',
            url: '/apiv1/inventory/items',
            data: JSON.stringify(info),
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}


function get_item(){
    id = 1
    $.ajax (
        {
            type: 'GET',
            url: '/apiv1/inventory/items/'+id,
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}


function add_vendor(){
    info = {
        'action':'add',
        "first_name": "one",
        'middle_name': "one",
        'last_name': "one",
        'email': "jlk@c.com",
        'website': "jasf",
        'tax_number': "sdf",
        'phone1': "sadfas",
        'phone2': "sdf",
        'address': "sdf"   
    }
    $.ajax (
        {
            type: 'POST',
            url: '/apiv1/inventory/vendors',
            data: JSON.stringify(info),
            success: function(data){
                console.log(data)
            },
            error: function(data){ 
                console.log(data)
            }
        });
}

