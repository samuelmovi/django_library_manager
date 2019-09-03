$(document).ready(function(){
    var banner = $("banner");
    if (banner){
        banner.click(function(){
        alert("Library!!");
    });
    }
    else{
        alert('No banner!!');
    };



});

/*
    // clickable rows in show books
    var bookRows = $("#books").find('.book-row');
    bookRows.each(function(){
        var rowID = $(this).attr('id');
        $(this).on('click', function(){
            //$(this).replaceWith('<a href="/books/modify/'+rowID+'/" />');
        });
    })

  // column sorting
    function sortBooks(){
        var bookInfoTable = $('#info');
        // var rows = bookInfoTable.children();
        var rows = bookInfoTable.find(".book-info");

    }

  // clickable rows in show books
    var bookRows = $("#books").children('tr');
    var i;
    for (i=0; i<bookRows.length; i++){
        alert("WQERWQER");
        var row = bookRows.eq(i);
        alert(row);
        var rowID = row.attr('id').split("-")[1];
        row.click(function(){
            window.location('google.com');
        })
        row.on('click', function(){
            $.get('/books/modify/'+row.attr('id'));
        })
    }
        var row;
    for (row in bookRows){
        var rowID = bookRows.eq(row).attr('id');
        row.on('click', function(){
            alert(rowID);
        });
    }

*/