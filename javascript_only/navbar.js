function loadNavbar(){
	nav = document.getElementById('navbar');
	nav.innerHTML = '<nav>\
	<ul class="horizontal-list">\
		<li><a href="jobs.html">Jobs</a></li>\
		<li><a href="core.html">Cores</a></li>\
		<li><a href="layer.html">Layers</a></li>\
	</ul>\
	</nav>\
	';
    links = nav.getElementsByTagName('a');
	currentPage =  window.location.href.split('?')[0];//don't want query params here.
	console.log(currentPage);
	//set style to current for current page.
	for(let i = 0;i < links.length; i++)
	{
		a = links[i];
		if (a.href == currentPage){a.className = 'current-page';}
	}
}