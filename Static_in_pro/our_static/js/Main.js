//upload file and verify that it is an excel sheet.
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


//use the drag and drop event of HTML5
//this function allow the drop of event in any container
function allowDrop(event) {
    event.preventDefault();
}

//drag function to enable the drag and drop of an elment
//during the drag save the information for the drag element
function drag(e, event) {
    event.dataTransfer.setData("Text", $(e).attr("value")); //set the text of the drag element
    event.dataTransfer.setData("item", event.target.id);   //get the dragged element
    event.dataTransfer.setData("id", $(e).attr("id"));

    //remove the element from the first container
    $(e).parent().find('input').filter(function () {
        return this.id == $(e).attr("id")
    }).remove()
}

//drag and drop event is created for list item. The problem with list item that
//they can not be send to the server so we should create input element
//for each dropped element
//the name of the input field should have the same name of the dragged element
//the name of the dragged element represent INf,QF, or Product details

function drop(e, event) {
    event.preventDefault();
    $("#copyInput").attr("name", $(e).attr("name")); //get the hidden input filed and set its name to the drop element name
    var clone = $("#copyInput").clone(); // copy the element using clone method
    //use the dataTransfer.getData to get the data that you have sat in the setData
    //during the drag event
    $(clone).attr("value", event.dataTransfer.getData("Text"));
    $(clone).attr("id", event.dataTransfer.getData("id"));

    //append the dragged element to the container and append the input field
    var dataItem = event.dataTransfer.getData("item");
    $(e).append(document.getElementById(dataItem));
    $(e).append(clone);

}


//move to influencing factors function
//this function is used to transfer all the data that are in the main category container
//to the INF containers
function onClick() {

    //get the main category that include all the column names
    var ulm = document.getElementById("ML");
    //get the influencing factor container
    var ul = document.getElementById("InflFactor");
    //get the list that are inside the INF
    var listItem = ulm.getElementsByTagName("li");
    //loop through all the list elements to create
    // input fileds for them, so they can be send to the server.
    //then append the item to the INF container, so it will be
    //removed form the general container to INF container

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
//this function is created to remove the extra added categories
//in the Batch page. The first element should not be deleted always
//to know the first element it always has the duplicterD id without extra number
//when we delete element it could be either in the date, string or decimal category
//each category should be manipulated alone. The operation field that is added with
//the category should be removed also
function onClickremove(t, e, event) {
    event.preventDefault();
    //remove decimal control
    if (t == "after-add-more-DF") {
        if ($(e).closest('.after-add-more-DF').attr("id") != "duplicaterD") {
            var ido = $(e).closest('.after-add-more-DF').attr('id');
            ido = "s" + ido;
            var op = document.getElementById(ido);
            $(op).remove();
            $(e).closest('.after-add-more-DF').remove();

        }
    }
    //remove string control
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

    //remove datetime control
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

    //display the datetimepicker and assign the selected date to the input field on change or on update
    $(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii:ss'}).on('dp.change dp.update', function () {
        $(".form_datetime").find("input").eq(1).attr("value", $(".form_datetime").data("DateTimePicker").date())

    });


    //display the influencing factor filter criteria in the group page
    $('#InfCheckBox').change(function () {
        $('#InfluncingFactorDetails').toggle();
    });
    $('#InfCheckBox').on('click', function () {
        $(this).val(this.checked ? 1 : 0);

    });

    //to let the user decide if he wants to select product or not
    $('#Noselectcb').on('click', function () {
        $(this).val(this.checked ? 1 : 0);

    });


    //if the user enter the number of samples he/she wants for each product,
    //select products that have the same number of samples in the product tables in
    //group page
    $('#SampleN').change(function () {
        table.rows({'search': 'applied'}).every(function (rowIdx, tableLoop, rowLoop) {

            var rowNode = this.node();
            var total = $(rowNode).find("td.total").text();
            var SampleN = $('#SampleN').val();

            if (total == SampleN) {
                $(rowNode).find('input[type="checkbox"]').prop('checked', 'checked');
                $(rowNode).find('input[type="checkbox"]').prop('name', 'CKT');
            }
            if (total != SampleN) {
                $(rowNode).find('input[type="checkbox"]').prop('checked', '');
                $(rowNode).find('input[type="checkbox"]').prop('name', 'CKF');

            }
        });

    });


    //set the active menu element to the current page element
    $(".nav-item a").on("click", function () {
        $(".nav-item").find(".active").removeClass("active");
        $(this).parent().addClass("active");
    });

    //enable search in datatables control
    $('#search').multiselect({
        search: {
            left: '<input type="text" name="q" class="form-control" placeholder="Search..." />',
            right: '<input type="text" name="q" class="form-control" placeholder="Search..." />',
        },
        fireSearch: function (value) {
            return value.length > 3;
        }
    });


    //batch detail Table
    var $table = $('#myTable');


    //enable the expand or row to display product detail
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

    //DataTable enable the search in the bottom of the table

    $('#example tfoot th').each(function () {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Search ' + title + '" />');
    });

    // DataTable
    var table = $('#example').DataTable({
        columnDefs: [{
            'targets': 0,
            'searchable': false,
            'orderable': false,
            'className': 'dt-body-center',
            'render': function (data, type, full, meta) {
                return '<input type="checkbox" id="CK" name="id[]" class="edit" value="'
                    + $('<div/>').text(data[9]).html() + '">';
            } //add input field in side the checkbox td
        },
            {"visible": false, "targets": 5},
            {"visible": false, "targets": 8},
            {"visible": false, "targets": 9},
            {"visible": false, "targets": 10},
            {"visible": false, "targets": 11},
        ],
        'select': {
            'style': 'multi'
        },

        "order": [[5, 'asc']],
        "displayLength": 25,
        "fnRowCallback": function (nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            if (aData[7] > 1) {
                $('td', nRow).css('background-color', '#FFAB91');
               //color the product rows that has more than one sample
            }
            else {
                // $('td', nRow).css('background-color', 'White');
            }
            //set the value of the input field inside checkbox
            $('td', nRow).find('input').attr('value', aData[9]);

        },
        "drawCallback": function (settings) {
            var api = this.api();
            var rows = api.rows({page: 'current'}).nodes();
            var last = null;
            //create group of batches inside the table, so the products will be displayed under each batches
            api.column(5, {page: 'current'}).data().each(function (group, i) {
                if (last !== group) {
                    $(rows).eq(i).before(
                        '<tr class="group" style="background-color:#17a2b8;color: white "><td colspan="7">' + group + '</td></tr>'
                    );

                    last = group;
                }
            });

        },
        "deferRender": true
    });


    // Order by the grouping
    $('#example tbody').on('click', 'tr.group', function () {
        var currentOrder = table.order()[0];
        if (currentOrder[0] === 5 && currentOrder[1] === 'asc') {
            table.order([5, 'desc']).draw();
        }
        else {
            table.order([5, 'asc']).draw();
        }
    });


    //enable the select all function in the datatable
    $('#example-select-all').on('click', function () {

        // Check/uncheck all checkboxes in the table
        var rows = table.rows({'search': 'applied'}).nodes();
        $('input[type="checkbox"]', rows).prop('checked', this.checked);

        if (this.checked) {
            $('input[type="checkbox"]', rows).prop('name', 'CKT');
            //set the name of the checkbox input CKT which mean that the
            //check box has been checked for render purpose

        }
        else {

            $('input[type="checkbox"]', rows).prop('name', 'CKF');
            //set the name of the checkbox input CKF which mean that the
            //check box has been not  checked for render purpose
        }
    });


    // Handle click on checkbox to set state of "Select all" control
    $('#example tbody').on('change', 'input[type="checkbox"]', function () {
        var row = $(this).closest('tr');
        if (this.checked) {
            $(this).attr('name', 'CKT');
        }
        else {

            $(this).attr('name', 'CKF');
        }

        // If checkbox is not checked
        if (!this.checked) {
            var el = $('#example-select-all').get(0);
            // If "Select all" control is checked and has 'indeterminate' property
            if (el && el.checked && ('indeterminate' in el)) {
                // Set visual state of "Select all" control
                // as 'indeterminate'
                el.indeterminate = true;
            }
        }
    });



    // Apply the search
    table.columns().every(function () {
        var that = this;

        $('input', this.footer()).on('keyup change', function () {
            if (that.search() !== this.value) {
                that
                    .search(this.value)
                    .draw();
            }
        });
    });

    $.fn.dataTableExt.ofnSearch['html'] = function (sData) {
        return $(sData).val();
    }

    // only displays the row that has the same number of the entered sample
    //or greater than
    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
            var min = parseInt($('#SampleN').val(), 10);

            var SampleNum = parseFloat(data[7]) || 0; // use data for the total column

            if (( isNaN(min)) || ( min <= SampleNum )) {

                return true;
            }
            return false;
        }
    );

    var table = $('#example').DataTable();

    //redraw the table after filtering according to the sample number
    $('#SampleN').keyup(function () {

        table.draw();

    });


});

function GetMaxSampN(e) {
    e.preventDefault();
    //get the highest number of total product(sample number)
    var table = $('#example').DataTable();
    var nextSeqNum = table
        .column(7)
        .data()
        .sort()
        .reverse()[0];
    var col3 = nextSeqNum;

    //get the entered sample number
    var sampNo = $('#SampleN').val();

    var mymodal = $('#model1');
    mymodal.find('.modal-body').text('');

    //if the sample numbers of one of the product greater than 1
    //and the user did not enter the sample number that he wants
    //display message that only one sample will be taken for each product
    if ((nextSeqNum > 1 && ($('#SampleN').val() == ''))) {
        mymodal.find('.modal-body').text('You did not Select any Product. The products will be selected in order.');
        mymodal.find('.modal-body').text('You did not enter the number of samples for each product. One measurement will be taken for each product.');
        mymodal.modal('show');
    }
    //if the user did not select product the product will be selected in order
    else if ((nextSeqNum > 1 && ($('#Noselectcb').val() == 1))) {
        mymodal.find('.modal-body').text('You did not Select any Product. The products will be selected in order.');
        mymodal.modal('show');
    }


    //if the user select products that he wants to process, do the following
    var countCk = 0; // count the selected row
    var numrow = table.rows({filter: 'applied'}).nodes().length; //get the number of row in the table
    var data = table.rows({filter: 'applied'}).data(); //get the data after applying any filter

   //create array that should hold the selected data
    var arr = new Array(numrow);
    for (i = 0; i < numrow; i++)
        arr[i] = new Array(8)

    //retrive the data from the datatable
    var i = 0;
    data.each(function (value, index) {
        arr[i][0] = index;  //rowNum
        arr[i][1] = data[index][1];  //productName
        arr[i][2] = data[index][11]; //QualityFeatureName
        arr[i][3] = data[index][10]; //batchID
        arr[i][4] = data[index][9]; //productId
        arr[i][5] = data[index][5]; //BatchName
        arr[i][7] = data[index][8]; //BatchProductID
        i++;

    });
    var seleIndex = [];
    var j = 0;
    //get the selected data from table
    var data = table.rows({filter: 'applied'}).nodes();
    $.each(data, function (index, value) {

        console.log($(this).find('input').prop('checked'));

        if ($(this).find('input').prop('checked')) {
            countCk = countCk + 1;
            seleIndex[j] = index;
            j++;
        }
    });

    for (i = 0; i < numrow; i++)
        for (j = 0; j < seleIndex.length; j++) {
            if (arr[i][0] == seleIndex[j]) {
                arr[i][6] = 'Selected';
            }

        }

    //get the selected products inside each batch and make sure it
    //equals the same number of entered sample, otherwise
    //display error
    var selectedP = [];
    if ((nextSeqNum > 1 && ($('#Noselectcb').val() == 0))) {
        if (countCk > 0) {
            for (i = 0; i < numrow; i++) {
                var np = 0;
                for (j = 0; j < numrow; j++) {
                    if (arr[i][3] == arr[j][3] && arr[i][1] == arr[j][1]) {

                        //alert('inside j loop before select ' + arr[j][0] + arr[i][5] + arr[i][1]);
                        if (arr[j][6] == 'Selected') {
                            np++;
                            selectedP.push(arr[j][7]);
                            //   alert('inside j loop selected '  + arr[j][0]  + arr[i][5] + arr[i][1] +arr[j][6] + arr[j][7]);
                        }
                    }
                }

                //alert ('outside j loop ' + arr[i][5] + arr[i][1] + np ) ;
                if (sampNo != np) {
                    //alert('modalError') ;
                    var mymodalEr = $('#modalError');
                    mymodalEr.find('.modal-body').text('');
                    mymodalEr.find('.modal-body').text('You selected wrong number of product for Batch : ' + arr[i][5] + ', Product: ' + arr[i][1]);
                    mymodalEr.modal('show');
                    break;

                }

            }
        }

        var outputArray = [];
        //get the selected proudct if the number is correct and add input field to send them
        //when the form is submitted
        for (var i = 0; i < selectedP.length; i++) {
            if ((jQuery.inArray(selectedP[i], outputArray)) == -1) {
                outputArray.push(selectedP[i]);
                $('#ProductDetailT').append('<input type="hidden" name="SelectedBatchProduct" value="' + selectedP[i] + '">');
            }
        }
    }
    if ($('#SampleN').val() && countCk == 0) {
        mymodal.find('.modal-body').text('You did not Select any Product. The products will be selected in order.');
        mymodal.modal('show');
    }

    $('#ProductDetailT').append('<input type="hidden" name="SubmitGroupProductDetail" value="SubmitGroupProductDetail" />');
    $('#ProductDetailT').submit();

}

$('#SubmitGroupProductDetail').click(function () {
    /* when the submit button in the modal is clicked, submit the form */
    //add input field to know which form to process
    $('#ProductDetailT').append('<input type="hidden" name="SubmitGroupProductDetail" value="SubmitGroupProductDetail" />');
    $('#ProductDetailT').submit();
});

var id = 0, is = 0, idt = 0;
var original = document.getElementById('duplicater');

//add new controls for influencing factors filter
//when the plus button is pressed
function duplicate(t, e, event) {
    event.preventDefault();
  //add decimal controls
    if (t == "after-add-more-DF") {
        var operation = document.getElementById('AndOrFDF');
        var cloneOp = operation.cloneNode(true);
        var original = document.getElementById('duplicaterD');
        var clone = original.cloneNode(true); // "deep" clone
        clone.id = "duplicaterD" + ++id;
        cloneOp.id = "s" + clone.id;
        cloneOp.hidden = false;
        $(clone).find("input:text").val(""); //set the value of the newly created element to empty
        // or clone.id = ""; if the divs don't need an ID
        $(clone).insertAfter("#" + $(e).closest('.after-add-more-DF').attr("id"));
        $(cloneOp).insertBefore("#" + $(clone).attr('id'));
    }
    //add string controls
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

        var sub = document.getElementsByClassName("InfluencingFactorV")[countinfS];
        for (var i = 0; i < sub.length; i++) {
            sub.options[i].hidden = true;
        }


    }
    //add date controls
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
            format: 'yyyy-mm-dd hh:ii:ss'
        });
    }
}

$(function () {
    bs_input_file();
    setNavigation();
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


//if the user select string influencing factor, display the value that are
//related to this selection
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

//when adding extra date field in the batch page clear the text of newely added field
function ClearRelatedTextBox(e, d) {
    if (d == "Date1") {
        $(e).parent().find('input.Date1').attr('value', '');

    }
    else
        $(e).parent().find('input.Date2').attr('value', '');
}

//set the current active menu element to the current page
function setNavigation() {
    var links = $('.navbar ul li a');
    $.each(links, function (key, va) {
        if (va.href == document.URL) {
            $(this).addClass('active');
        }
    });
}


//$('#move_INF').click(function() {
//    $('.InflFactor').append($('.ML .selected').removeClass('selected'));
//});



