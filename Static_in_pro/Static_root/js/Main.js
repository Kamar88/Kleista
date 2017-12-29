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
var countinfS = 0 ;

function onClickremove(t, e, event) {
    event.preventDefault();
    if(t == "after-add-more-DF"){
    if ($(e).closest('.after-add-more-DF').attr("id") != "duplicaterD") {
        var ido = $(e).closest('.after-add-more-DF').attr('id');
        ido = "s" + ido ;
        var op = document.getElementById(ido);
        $(op).remove() ;
        $(e).closest('.after-add-more-DF').remove();

    }}
    if(t == "after-add-more-S"){
    if ($(e).closest('.after-add-more-S').attr("id") != "duplicaterS") {
        var ido = $(e).closest('.after-add-more-S').attr('id');
        ido = "s" + ido ;
        var op = document.getElementById(ido);
        $(op).remove() ;
        $(e).closest('.after-add-more-S').remove();
        --countinfS ;
    }}
     if(t == "after-add-more-DT"){
    if ($(e).closest('.after-add-more-DT').attr("id") != "duplicaterDT") {
        var ido = $(e).closest('.after-add-more-DT').attr('id');
        ido = "s" + ido ;
        var op = document.getElementById(ido);
        $(op).remove() ;
        $(e).closest('.after-add-more-DT').remove();
    }}


}



$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
    $('.js-example-basic-single').select2();
   // $('.input-daterange').datepicker({
//});
      $(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii'});

});



var id = 0, is=0, idt=0;
var original = document.getElementById('duplicater');



function duplicate(t, e, event) {
    event.preventDefault();

 if(t == "after-add-more-DF"){
     var operation = document.getElementById('AndOrFDF');
     var cloneOp = operation.cloneNode(true);
     var original = document.getElementById('duplicaterD');
     var clone = original.cloneNode(true); // "deep" clone
     clone.id = "duplicaterD" + ++id;
     cloneOp.id = "s" + clone.id ;
     cloneOp.hidden = false ;
    // or clone.id = ""; if the divs don't need an ID
    $(clone).insertAfter("#" + $(e).closest('.after-add-more-DF').attr("id"));
    $(cloneOp).insertBefore("#" + $(clone).attr('id'));
 }
    if(t == "after-add-more-S"){
     var operation = document.getElementById('AndOrFS');
     var cloneOp = operation.cloneNode(true);
     var originalS = document.getElementById('duplicaterS');
     var clone = originalS.cloneNode(true); // "deep" clone
     clone.id = "duplicaterS" + ++is;
     cloneOp.id = "s" + clone.id ;
     cloneOp.hidden = false ;
     ++countinfS ;
     var childOption = clone.getElementsByTagName('Select') ;
    // or clone.id = ""; if the divs don't need an ID
    $(clone).insertAfter("#" + $(e).closest('.after-add-more-S').attr("id"));
    $(cloneOp).insertBefore("#" + $(clone).attr('id'));}
    if(t == "after-add-more-DT"){
        var operation = document.getElementById('AndOrFDa');
     var cloneOp = operation.cloneNode(true);
        var originalS = document.getElementById('duplicaterDT');
     var clone = originalS.cloneNode(true); // "deep" clone
     clone.id = "duplicaterDT" + ++is;
      cloneOp.id = "s" + clone.id ;
     cloneOp.hidden = false ;
    // or clone.id = ""; if the divs don't need an ID
    $(clone).insertAfter("#" + $(e).closest('.after-add-more-DT').attr("id"));
    $(cloneOp).insertBefore("#" + $(clone).attr('id'));
    $(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii'});
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

function OnChangeIS(e){
        var val = $(e).val();
        var idn = $(e).attr("id") ;
        var sub = document.getElementsByClassName("InfluencingFactorV")[countinfS];
        for (var i=0; i<sub.length; i++){
            if(sub.options[i].id == val && sub.options[i].value !== '')
                sub.options[i].hidden = false ;
            else
                sub.options[i].hidden = true ;
        }

}



//$('#move_INF').click(function() {
//    $('.InflFactor').append($('.ML .selected').removeClass('selected'));
//});



