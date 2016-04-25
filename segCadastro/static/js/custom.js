/**************************************************************

Form Wizard

***************************************************************/
$(document).ready(function () {
    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();

    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {

        var $target = $(e.target);

        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);

    });
    $(".prev-step").click(function (e) {

        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);

    });
});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}

/**************************************************************

Search Select Multiple

***************************************************************/

$(document).ready(function() {
  $(".js-example-basic-single").select2();
});

/**************************************************************

Adicionar Itens AFE

***************************************************************/
$(document).ready(function () {
    // Code adapted from http://djangosnippets.org/snippets/1389/
    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function deleteForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.itemA').remove();
            var forms = $('.itemA'); // Get all the forms
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            var i = 0;
            // Go through the forms and set their indices, names and IDs
            for (formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).children().children().each(function () {
                    if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            alert("You have to enter at least one todo item!");
        }
        return false;
    }

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        // You can only submit a maximum of 10 todo items
        if (formCount < 10) {
            // Clone a form (without event handlers) from the first form
            var row = $(".itemA:first").clone(false).get(0);
            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".itemA:last").slideDown(300);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");

            // Relabel or rename all the relevant bits
            $(row).children().children().each(function () {
                updateElementIndex(this, prefix, formCount);
                $(this).val("");
            });

            // Add an event handler for the delete item/form link
            $(row).find(".delete").click(function () {
                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        } // End if
        else {
            alert("Sorry, you can only enter a maximum of ten items.");
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
        return addForm(this, "formaf");
    });

    $(".delete").click(function () {
        return deleteForm(this, "formaf");
    });
});
/**************************************************************

Adicionar Preload

***************************************************************/
jQuery(window).load(function() {
   // Page Preloader
   jQuery('#status').fadeOut();
   jQuery('#preloader').delay(350).fadeOut(function(){
      jQuery('body').delay(350).css({'overflow':'visible'});
   });
});

/**************************************************************

jQuery UI - Autocomplete

***************************************************************/
$(function() {
  $( "#autocomplete-processo" ).autocomplete({
    source: "/autocomplete/service/",
    focus: function( event, ui ) {
      $( "#autocomplete-processo" ).val( ui.item.name );
      return false;
    },
    select: function( event, ui ) {
      $( "#autocomplete-processo" ).val( ui.item.name );
      $( "#processo-id" ).val( ui.item.id );
      return false;
    }
  })
  .autocomplete( "instance" )._renderItem = function( ul, item ) {
    return $( "<li>" )
      .append( "<a>" + item.name + "</a>" )
      .appendTo( ul );
  };
});
