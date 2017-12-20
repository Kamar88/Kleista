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

function onClickremove(t, e, event) {
    event.preventDefault();
    if(t == "after-add-more-DF"){
    if ($(e).closest('.after-add-more-DF').attr("id") != "duplicaterD") {
        $(e).closest('.after-add-more-DF').remove();
    }}
    if(t == "after-add-more-S"){
    if ($(e).closest('.after-add-more-S').attr("id") != "duplicaterS") {
        $(e).closest('.after-add-more-S').remove();
    }}
     if(t == "after-add-more-DT"){
    if ($(e).closest('.after-add-more-DT').attr("id") != "duplicaterDT") {
        $(e).closest('.after-add-more-DT').remove();
    }}


}

$('.select-decimal').selectize({
					maxItems: 3
				});


var id = 0, is=0, idt=0;
var original = document.getElementById('duplicater');

function duplicate(t, e, event) {
    event.preventDefault();

 if(t == "after-add-more-DF"){
     var original = document.getElementById('duplicaterD');
     var clone = original.cloneNode(true); // "deep" clone
     clone.id = "duplicaterD" + ++id;
    // or clone.id = ""; if the divs don't need an ID
    $(clone).insertAfter("#" + $(e).closest('.after-add-more-DF').attr("id"));}
    if(t == "after-add-more-S"){
     var originalS = document.getElementById('duplicaterS');
     var clone = originalS.cloneNode(true); // "deep" clone
     clone.id = "duplicaterS" + ++is;
    // or clone.id = ""; if the divs don't need an ID
    $(clone).insertAfter("#" + $(e).closest('.after-add-more-S').attr("id"));}
    if(t == "after-add-more-DT"){
        var originalS = document.getElementById('duplicaterDT');
     var clone = originalS.cloneNode(true); // "deep" clone
     clone.id = "duplicaterDT" + ++is;
    // or clone.id = ""; if the divs don't need an ID
    $(clone).insertAfter("#" + $(e).closest('.after-add-more-DT').attr("id"));}
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

//$('#move_INF').click(function() {
//    $('.InflFactor').append($('.ML .selected').removeClass('selected'));
//});



