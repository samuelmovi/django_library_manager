$(document).ready(function(){

    // CLICKABLE TABLE HEADINGS
    $('th').click(function(){
        var table = $(this).parents('table').eq(0)
        var rows = table.find('tr:gt(0)').toArray().sort(compare($(this).index()))
        this.asc = !this.asc
        if (!this.asc){rows = rows.reverse()}
        for (var i = 0; i < rows.length; i++){
            table.append(rows[i])
        }
    })
    function compare(index) {
        return function(a, b) {
            var valA = getCellValue(a, index), valB = getCellValue(b, index)
            return $.isNumeric(valA) && $.isNumeric(valB) ? valA - valB : valA.toString().localeCompare(valB)
        }
    }
    function getCellValue(row, index){
        return $(row).children('td').eq(index).text()
    }

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