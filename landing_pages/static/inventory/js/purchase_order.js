$( document ).ready(function() {
    getStatus();
    getPurchaseOrder(0,10);
    $("#purchase_order_modify").hide();
});



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

function notify_error(data)
{
    swal("An unexpected error occured, Please report to the devs. Error : "+data['error'], {
        dangerMode: true,
        buttons: {
            confirm: true,
        },
        })
}


function getPurchaseOrder(start, end)
{
    var xhttp = new XMLHttpRequest();
    info = {
        'action':'get',
        'start':start,
        'end':end,
        'filter':'none',
    }
    $.ajax ({
        type: 'POST',
        url: '/apiv1/inventory/porders',
        data:JSON.stringify(info),
        success: function(data){
            process_data(data)
        },
        error:function(data){
            notify_error(data)
        }
    });

}

function getStatus(){
    var xhttp = new XMLHttpRequest();
    $.ajax ({
        type: 'GET',
        url: '/apiv1/inventory/status',
        success: function(data){
            outputData(data);     
    },
    error: function(data){
            notify_error(data)
        }
    });

    function outputData(data){
        y = data['data'].length;
        data = data['data']
        while (y) {
        y = y -1;
        $("#select_status").append(
            '<option value = '+data[y]['id']+'>'+data[y]['name']+'</option>'
        )
    }
    }
}


function getPurchaseOrderUsingStatus(status,start,end)
{
    var xhttp = new XMLHttpRequest();
    info = {
        'action':'get',
        'start':start,
        'end':end,
        'filter':'status',
        'status_id':status
    }
    $.ajax ({
        type: 'POST',
        url: '/apiv1/inventory/porders',
        data:JSON.stringify(info),
        success: function(data){
            process_data(data)
        },
        error:function(data){
            notify_error(data)
        }
    });

}

function getSelectedOrder(id)
{
    var xhttp = new XMLHttpRequest();
    $.ajax ({
        type: 'GET',
        url: '/apiv1/inventory/porders/'+id,
        success: function(data){
            processSinglePurchaseOrder(data);
            console.log(data);        
    }
    }); 
}
function processSinglePurchaseOrder(data)
{
    $("#order_table").hide();
    $("#purchase_order_modify").show();
    
}

function process_data(data)
{
    if (data['status'])
    {
        data = data['p_orders']
        y  = data.length
        $("tr").remove(".table-row");
        while (y) {
            y = y -1;
            $("#order_results").append(
                '<tr data-href="'+data[y]['id']+'" class="table-row"><td>'+data[y]['vendor_name'] +'</td><td>'+data[y]['items'] +'</td><td>'+data[y]['invoiced_on'] +'</td><td>'+data[y]['completed_on'] +'</td><td>'+data[y]['total_cost'] +'</td><td>'+data[y]['status_name'] +'</td></tr>'
            )
        }
        $(".table-row").click(function() {
        x = $(this).data("href");
        getSelectedOrder(x);
        });
    }
    else{
        notify_error(data);
    }
    
    $("#purchase_order_modify").hide();
    $("#order_table").show();
}


