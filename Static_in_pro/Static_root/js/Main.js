function bs_input_file() {
    $(".input-file").before(
        function () {
            if (!$(this).prev().hasClass('input-ghost')) {
                var element = $("<input type='file' accept='.xls,.xlsx' class='input-ghost' style='visibility:hidden; height:0'>");
                element.attr("name", $(this).attr("name"));
                element.change(function () {
                    element.next(element).find('input').val((element.val()).split('\\').pop());
                });
                $(this).find("button.btn-choose").click(function () {
                    element.click();
                });
                $(this).find("button.btn-reset").click(function () {
                    element.val(null);
                    $(this).parents(".input-file").find('input').val('');
                });
                $(this).find('input').css("cursor", "pointer");
                $(this).find('input').mousedown(function () {
                    $(this).parents('.input-file').prev().click();
                    return false;
                });
                return element;
            }
        }
    );
}

function allowDrop(event) {
    event.preventDefault();
}

function drag(e, event) {
    //alert($(e).attr("value"));
    //alert($(e).attr("id"));
    event.dataTransfer.setData("Text", $(e).attr("value"));
    event.dataTransfer.setData("item", event.target.id);
    event.dataTransfer.setData("id", $(e).attr("id"));
    //$(e).parent().find('input#copyInput').filter(function () {return this.name == $(e).attr("id")
    $(e).parent().find('input').filter(function () {
        return this.id == $(e).attr("id")
    }).remove()
}

function drop(e, event) {
    event.preventDefault();
    //alert($(e).attr("name"));
    $("#copyInput").attr("name", $(e).attr("name"));
    var clone = $("#copyInput").clone();
    $(clone).attr("value", event.dataTransfer.getData("Text"));
    //$(clone).attr("name", $(e).attr("name"));
    $(clone).attr("id", event.dataTransfer.getData("id"));
    //alert(event.dataTransfer.getData("Text"));
    var dataItem = event.dataTransfer.getData("item");
    $(e).append(document.getElementById(dataItem));
    $(e).append(clone);

}

function onClick() {

    var ulm = document.getElementById("ML");
    var ul = document.getElementById("InflFactor");
    var listItem = ulm.getElementsByTagName("li");
    //("#ML").appendTo("#InflFactor");
    //alert(listItem.length)
    while (listItem.length > 0) {
        for (var i = 0; i < listItem.length; i++) {
            var clone = $("#copyInput").clone();
            $(clone).attr("value", $(listItem[i]).attr("value"));
            $(clone).attr("id", $(listItem[i]).attr("id"));
            $(clone).attr("name", "InflFactor");
            //alert(event.dataTransfer.getData("Text"));
            $("#InflFactor").append(clone);
            $("#InflFactor").append(listItem[i]);
        }
    }

}

$(document).on('click', '.btn-add', function (e) {
    alert('add')
    e.preventDefault();

    var controlForm = $('.controls form:first'),
        currentEntry = $(this).parents('.entry:first'),
        newEntry = $(currentEntry.clone()).appendTo(controlForm);

    newEntry.find('input').val('');
    controlForm.find('.entry:not(:last) .btn-add')
        .removeClass('btn-add').addClass('btn-remove')
        .removeClass('btn-success').addClass('btn-danger')
        .html('<span class="glyphicon glyphicon-minus"></span>');
}).on('click', '.btn-remove', function (e) {
    $(this).parents('.entry:first').remove();

    e.preventDefault();
    return false;
});
var countinfS = 0;

function onClickremove(t, e, event) {
    event.preventDefault();
    if (t == "after-add-more-DF") {
        if ($(e).closest('.after-add-more-DF').attr("id") != "duplicaterD") {
            var ido = $(e).closest('.after-add-more-DF').attr('id');
            ido = "s" + ido;
            var op = document.getElementById(ido);
            $(op).remove();
            $(e).closest('.after-add-more-DF').remove();

        }
    }
    if (t == "after-add-more-S") {
        if ($(e).closest('.after-add-more-S').attr("id") != "duplicaterS") {
            var ido = $(e).closest('.after-add-more-S').attr('id');
            ido = "s" + ido;
            var op = document.getElementById(ido);
            $(op).remove();
            $(e).closest('.after-add-more-S').remove();
            --countinfS;
        }
    }
    if (t == "after-add-more-DT") {
        if ($(e).closest('.after-add-more-DT').attr("id") != "duplicaterDT") {
            var ido = $(e).closest('.after-add-more-DT').attr('id');
            ido = "s" + ido;
            var op = document.getElementById(ido);
            $(op).remove();
            $(e).closest('.after-add-more-DT').remove();
        }
    }


}


$(document).ready(function () {
    $('.js-example-basic-multiple').select2();
    $('.js-example-basic-single').select2();
    // $('.input-daterange').datepicker({
//});
    //display the datetimepicker and assign the selected date to the input field on change or on update
    $(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii'}).on('dp.change dp.update', function () {
        $(".form_datetime").find("input").eq(1).attr("value", $(".form_datetime").data("DateTimePicker").date())

    });

    $('#InfCheckBox').change(function () {
        $('#InfluncingFactorDetails').toggle();
    });
    $('#InfCheckBox').on('click', function () {
        $(this).val(this.checked ? 1 : 0);

    });

    $('#search').multiselect({
        search: {
            left: '<input type="text" name="q" class="form-control" placeholder="Search..." />',
            right: '<input type="text" name="q" class="form-control" placeholder="Search..." />',
        },
        fireSearch: function (value) {
            return value.length > 3;
        }
    });

    var $table = $('#myTable');

    $table.on('expand-row.bs.table', function (e, index, row, $detail) {
        var res = $("#desc" + index).html();
        $detail.html(res);
    });

    $table.on("click-row.bs.table", function (e, row, $tr) {

        // prints Clicked on: table table-hover, no matter if you click on row or detail-icon
        console.log("Clicked on: " + $(e.target).attr('class'), [e, row, $tr]);

        // In my real scenarion, trigger expands row with text detailFormatter..
        //$tr.find(">td>.detail-icon").trigger("click");
        // $tr.find(">td>.detail-icon").triggerHandler("click");
        if ($tr.next().is('tr.detail-view')) {
            $table.bootstrapTable('collapseRow', $tr.data('index'));
        } else {
            $table.bootstrapTable('expandRow', $tr.data('index'));
        }
    });

    $('#example tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );

    // DataTable
    var table =  $('#example').DataTable( {
        columnDefs: [ {
            orderable: false,
            targets:   0 ,
            'checkboxes': {
               'selectRow': true
            }
        } ,
          { "visible": false, "targets": 5 }

        ],
        'select': {
         'style': 'multi'
      },

        "order": [[ 5, 'asc' ]],
        "displayLength": 25,
        "drawCallback": function ( settings ) {
            var api = this.api();
            var rows = api.rows( {page:'current'} ).nodes();
            var last=null;

            api.column(5, {page:'current'} ).data().each( function ( group, i ) {
                if ( last !== group ) {
                    $(rows).eq( i ).before(
                        '<tr class="group"><td colspan="7">'+group+'</td></tr>'
                    );

                    last = group;
                }
            } );
        }
    } );







    // Order by the grouping
    $('#example tbody').on( 'click', 'tr.group', function () {
        var currentOrder = table.order()[0];
        if ( currentOrder[0] === 5 && currentOrder[1] === 'asc' ) {
            table.order( [ 5, 'desc' ] ).draw();
        }
        else {
            table.order( [ 5, 'asc' ] ).draw();
        }
    } );

   // Handle form submission event
   $('#frm-example').on('submit', function(e){
      var form = this;

      var rows_selected = table.column(0).checkboxes.selected();

      // Iterate over all selected checkboxes
      $.each(rows_selected, function(index, rowId){
         // Create a hidden element
         $(form).append(
             $('<input>')
                .attr('type', 'hidden')
                .attr('name', 'id[]')
                .val(rowId)
         );
      });
   });

    // Apply the search
    table.columns().every( function () {
        var that = this;

        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );


});


var id = 0, is = 0, idt = 0;
var original = document.getElementById('duplicater');


function duplicate(t, e, event) {
    event.preventDefault();

    if (t == "after-add-more-DF") {
        var operation = document.getElementById('AndOrFDF');
        var cloneOp = operation.cloneNode(true);
        var original = document.getElementById('duplicaterD');
        var clone = original.cloneNode(true); // "deep" clone
        clone.id = "duplicaterD" + ++id;
        cloneOp.id = "s" + clone.id;
        cloneOp.hidden = false;
        $(clone).find("input:text").val("");
        // or clone.id = ""; if the divs don't need an ID
        $(clone).insertAfter("#" + $(e).closest('.after-add-more-DF').attr("id"));
        $(cloneOp).insertBefore("#" + $(clone).attr('id'));
    }
    if (t == "after-add-more-S") {
        var operation = document.getElementById('AndOrFS');
        var cloneOp = operation.cloneNode(true);
        var originalS = document.getElementById('duplicaterS');
        var clone = originalS.cloneNode(true); // "deep" clon
        clone.id = "duplicaterS" + ++is;
        cloneOp.id = "s" + clone.id;
        cloneOp.hidden = false;
        ++countinfS;
        // or clone.id = ""; if the divs don't need an ID
        $(clone).insertAfter("#" + $(e).closest('.after-add-more-S').attr("id"));
        $(clone).find("select").attr("id", countinfS);
        $(cloneOp).insertBefore("#" + $(clone).attr('id'));
    }
    if (t == "after-add-more-DT") {
        var operation = document.getElementById('AndOrFDa');
        var cloneOp = operation.cloneNode(true);
        var originalS = document.getElementById('duplicaterDT');
        var clone = originalS.cloneNode(true); // "deep" clone
        $(clone).find("input:text").val("");
        clone.id = "duplicaterDT" + ++is;
        cloneOp.id = "s" + clone.id;
        cloneOp.hidden = false;
        // or clone.id = ""; if the divs don't need an ID
        $(clone).insertAfter("#" + $(e).closest('.after-add-more-DT').attr("id"));
        $(cloneOp).insertBefore("#" + $(clone).attr('id'));
        $(".form_datetime").datetimepicker({
            format: 'yyyy-mm-dd hh:ii'
        });
    }
}

$(function () {
    bs_input_file();

    $(document).on('click', '.btn-add', function (e) {
        e.preventDefault();

        var controlForm = $('.controls form:first'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<span class="glyphicon glyphicon-minus"></span>');
    }).on('click', '.btn-remove', function (e) {
        $(this).parents('.entry:first').remove();
        e.preventDefault();
        return false;
    });

});

function OnChangeIS(e, event) {
    var val = $(e).val();
    var idn = $(e).attr("id");
    var sub = document.getElementsByClassName("InfluencingFactorV")[idn];
    for (var i = 0; i < sub.length; i++) {
        if (sub.options[i].id == val && sub.options[i].value !== '')
            sub.options[i].hidden = false;
        else
            sub.options[i].hidden = true;
    }

}


function ClearRelatedTextBox(e, d) {
    if (d == "Date1") {
        $(e).parent().find('input.Date1').attr('value', '');

    }
    else
        $(e).parent().find('input.Date2').attr('value', '');

    //document.getElementById('dtp_input1').value = "";
}


//$('#move_INF').click(function() {
//    $('.InflFactor').append($('.ML .selected').removeClass('selected'));
//});



