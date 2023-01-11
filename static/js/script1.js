var frame_count = 1;  

$(document).ready(function()
{
    $('body').append($('<script src="static/js/md5.min.js"></script>'));
});

function add_row(elem)
{	
	var row_index = elem.parentElement.parentElement.children[0].rows.length - 1;
	var row = elem.parentElement.parentElement.children[0].rows[row_index];
    var table = elem.parentElement.parentElement.children[0];
    var clone = row.cloneNode(true);
	var cells_length = clone.cells.length - 1;
	for(var i = 1; i<cells_length; i++){
		clone.cells[i].children[0].value=""
	}
    table.appendChild(clone);
}

function delete_row(elem)
{
	if(elem.parentElement.parentElement.parentElement.rows.length > 2)
	{
		elem.parentElement.parentElement.remove();
	}else{
		alert("First row can not be deleted!")
	}
}

function uploadDocument()
{
	$("#uploadDocumentbtn").hide();
	var frame_list       = document.getElementsByClassName("frame");
	var basic_details    = {};
	var full_data        = {};
	var final_table_data = {};
	
	code_tbl  = frame_list[0].getElementsByClassName("code_tbl")[0]
	code_rows = code_tbl.rows
	for(var j = 1; j<code_rows.length; j++)
	{
		tds = code_rows[j].children		
		if (tds[0].firstElementChild.value=="")
		{	
				alert("DOCUMENT TYPE cannot be blank in row : "+j);$("#uploadDocumentbtn").show();
				return;
		}
		
		if (tds[1].firstElementChild.value=="")
		{	
				alert("VISIBILITY TYPE cannot be blank in row : "+j);$("#uploadDocumentbtn").show();
				return;
		}		
		if (tds[2].firstElementChild.value=="")
		{	
				alert("Comment cannot be blank in row : "+j);$("#uploadDocumentbtn").show();
				return;
		}	
		
	}
	for(var j = 1; j<code_rows.length; j++)
	{
		var table_data   			  = {};
		tds              			  = code_rows[j].children
		DOCUMENT_TYPE    			  = tds[0].firstElementChild.value
		VISIBILITY_TYPE  			  = tds[1].firstElementChild.value
		COMMENT          			  = tds[2].firstElementChild.value			
		table_data['DOCUMENT_TYPE']   = DOCUMENT_TYPE 
		table_data['VISIBILITY_TYPE'] = VISIBILITY_TYPE
		table_data['COMMENT']         = COMMENT
		final_table_data[j]           = table_data
	}
	
	full_data['observation']          = final_table_data
	full_data['basic_details']        = basic_details	
	$.post('/uploadDocument', 
	{
		params_data : JSON.stringify(full_data)
	}, function(result) 
	{
		alert(result.msg);
		$("#uploadDocumentbtn").show();		
	});	
}