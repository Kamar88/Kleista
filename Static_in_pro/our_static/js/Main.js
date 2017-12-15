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
    $(e).parent().find('input').filter(function () {return this.id == $(e).attr("id")
    }).remove()


}

function drop(e, event) {
    event.preventDefault();
    //alert($(e).attr("name"));
    $("#copyInput").attr("name",$(e).attr("name"));
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
    while (listItem.length > 0){
    for (var i = 0; i < listItem.length; i++) {
        var clone = $("#copyInput").clone();
        $(clone).attr("value",$(listItem[i]).attr("value"));
        $(clone).attr("id",$(listItem[i]).attr("id"));
        $(clone).attr("name","InflFactor");
        //alert(event.dataTransfer.getData("Text"));
         $("#InflFactor").append(clone);
         $("#InflFactor").append(listItem[i]);
    }}

}

//$('#move_INF').click(function() {
//    $('.InflFactor').append($('.ML .selected').removeClass('selected'));
//});

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


    //here first get the contents of the div with name class copy-fields and add it to after "after-add-more" div class.
    $(".add-more").click(function () {
        var html = $(".copy-fields").html();
        $(".after-add-more").after(html);
    });
//here it will remove the current value of the remove button which has been pressed
    $("body").on("click", ".remove", function () {
        $(this).parents(".copy-fields").remove();
    });

});

