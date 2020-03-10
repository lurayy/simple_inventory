
function search_vendor()
{
    search_text = $('#search_vendor').val()
    if (search_text.length > 3){
        $('#vendor_dropdown_data').show()
        $('#loader_id').show()
        search_text = search_text.charAt(0).toUpperCase() + search_text.slice(1).toLowerCase()
        var xhttp = new XMLHttpRequest();
        info = {
            'action':'get',
            'filter':'name',
            'first_name':search_text
        }
        $.ajax ({
            type: 'POST',
            url: '/apiv1/inventory/vendors',
            data:JSON.stringify(info),
            success: function(data){
                select_vendors(data)
                $('#loader_id').hide()
            },
            error:function(data){   
                $('#loader').hide()
                notify_error(data)
            }
        });
            
    }
    else {
        $('#vendor_dropdown_data').hide()
    }
}


function select_vendors(data){
    if (data['status'])
    {
        process_vendor_selection(data)
    }
    else{
        $('#no_data').remove()
        $("a").remove(".search_data");
        $("#vendor_dropdown_data").append(
            '<a id="no_data">No Data Found. Search only using First Name</a>'
        )
    }
}

function select_vendor(id,name)
{
    name = name.split('_').join(' ')
    $('#search_vendor').val(name)
    $('#vendor_dropdown_data').hide()
    console.log
}



function process_vendor_selection(data){
    data = data['vendors']
    y  = data.length
    $('#no_data').remove()
    $("a").remove(".search_data");
    while (y) {
        y = y -1;
        name = data[y]['first_name'] +' '+data[y]['middle_name'] + ' '+data[y]['last_name']
        console.log(name)
        send_name = name.split(' ').join('_')
        $("#vendor_dropdown_data").append(
            '<a onclick=select_vendor('+data[y]['id']+',"'+send_name+'") class="search_data">'+name+'</a>'
        )
    }
}




function purchase_order(data){
    console.log(data)   
}




