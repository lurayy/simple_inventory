$( document ).ready(function() {
    getStatus();
    getPurchaseOrder(0,10);
});

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



function getSelectedOrder(id)
{
    location.href=('/land/purchaseorder/'+id)
}