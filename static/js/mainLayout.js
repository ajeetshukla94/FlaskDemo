class MyHeader extends HTMLElement{
	
	connectedCallback()	{
		this.innerHTML ='<div id="header"> \
		<img src="static/images/logo.jpg" id="header-img"> \
		<h2 id="header-text">Document Manager</h2> \
		</div> \
		<div class="sidebar"> \
		<a id = "upload_document_link" href="/logout">UPLOAD DOCUMENT</a> \
		<a href="/logout">LOGOUT</a>  \
		</div>\
		'
		
	}
}
customElements.define('my-header',MyHeader)


class MyFooter extends HTMLElement{
	
	connectedCallback()	{
		this.innerHTML ='<div id="footer">\
			<h6 id="footer-text">Developed By &#169; Document Manager</h6>\
		</div>\
		'
	}
}
customElements.define('my-footer',MyFooter)